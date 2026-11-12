"""Generate an auditable runtime copy; preserve every upstream source file."""
import ast
import difflib
import hashlib
import os
from pathlib import Path


class RuntimePatch(ast.NodeTransformer):
    def __init__(self, config):
        self.config = config
        self.class_name = None
        self.function_name = None
        self.recovery_loops = 0
        self.full_vae = config.get("profile") == "paper_equations_v1"

    def visit_ClassDef(self, node):
        old = self.class_name
        self.class_name = node.name
        self.generic_visit(node)
        self.class_name = old
        return node

    def visit_FunctionDef(self, node):
        old = self.function_name
        self.function_name = node.name
        self.generic_visit(node)
        self.function_name = old
        return node

    def visit_ImportFrom(self, node):
        if node.module == "piq":
            return None
        return node

    def visit_Constant(self, node):
        replacements = {
            "stabilityai/stable-diffusion-3-medium-diffusers": self.config["model"],
            "pretrained_models/taesd3": self.config["tiny_vae"],
            "../../FLAIR/FLAIR-main/LCFM/SD3_loss_v_MSE_DIV2k_neg_prompt.npy":
                self.config["flair_regularizer"],
        }
        if isinstance(node.value, str) and node.value in replacements:
            node.value = replacements[node.value]
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        names = [ast.unparse(x) for x in node.targets]
        if "self.lpips_loss" in names:
            node.value = ast.Constant(None)  # Never read by any supported solver.
        if self.config["profile"] in {"paper_explicit_parameters", "paper_equations_v1"}:
            if self.class_name == "SD3FlowDPS" and "num_iters" in names:
                node.value = ast.Constant(3)
            if self.class_name == "SD3HDPS" and "num_iters_x" in names:
                node.value = ast.Constant(20)
        if names == ["pipe.vae"] and self.full_vae:
            return ast.parse("pipe.vae.to(dtype=torch.float32)\npipe.vae.requires_grad_(False)\npipe.vae.eval()").body
        if names == ["pipe.vae"]:
            return [node, *ast.parse(
                "pipe.vae.register_to_config(shift_factor=0.0)\n"
                "pipe.vae.requires_grad_(False)\npipe.vae.eval()").body]
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        if self.full_vae and isinstance(node.func, ast.Name) and node.func.id == "tqdm":
            node.keywords.append(ast.keyword(arg="disable", value=ast.Constant(True)))
        return node

    def visit_If(self, node):
        if self.full_vae and self.class_name == "SD3FLAIR" and any(isinstance(x, ast.Break) for x in ast.walk(node)):
            return None  # Appendix B.2 requests all 15 DC iterations.

        if (self.class_name == "SD3HDPS" and self.function_name == "sample"
                and self.config["profile"] == "paper_explicit_parameters"
                and any(isinstance(x, ast.Break) for x in ast.walk(node))
                and "42" in ast.unparse(node.test if "42" in ast.unparse(node.test) else node)):
            # The released code stops SR after 43/50 outer steps. Paper profile uses all 50.
            return None
        return self.generic_visit(node)

    def visit_For(self, node):
        self.generic_visit(node)
        supported = {"SD3HDPS": ["z", "z0y"],
                     "SD3FlowDPS": ["z"],
                     "SD3FLAIR": ["z0y", "z1t"]}
        direct = isinstance(node.iter, ast.Name) and node.iter.id == "pbar"
        enumerated = (isinstance(node.iter, ast.Call)
                      and isinstance(node.iter.func, ast.Name)
                      and node.iter.func.id == "enumerate"
                      and len(node.iter.args) == 1
                      and isinstance(node.iter.args[0], ast.Name)
                      and node.iter.args[0].id == "pbar")
        if (self.class_name not in supported or self.function_name != "sample"
                or not (direct or enumerated)):
            return node
        names = supported[self.class_name]
        # HDPS defines z0y during warm-start; retain it for a terminal-step restart.
        restore_names = names
        dictionary = "{" + ", ".join(repr(n) + ": " + n for n in restore_names) + "}"
        optimizers = "(optimizer_x, optimizer_z)" if self.class_name == "SD3FLAIR" else "()"
        before = ast.parse(
            "_resume_variables = " + dictionary + "\n"
            "_resume_step = _RECOVERY.restore(_resume_variables, " + optimizers + ")\n"
            + "\n".join(n + " = _resume_variables[" + repr(n) + "]" for n in restore_names)
        ).body
        node.body = ast.parse("if i < _resume_step:\n    continue").body + node.body
        node.body += ast.parse(
            "_RECOVERY.save(i + 1, " + dictionary + ", " + optimizers + ")").body
        self.recovery_loops += 1
        return before + [node]


def prepare(config, destination):
    original = (Path(config["repo"]) / "sd3_sampler.py").read_text(encoding="utf-8")
    patch = RuntimePatch(config)
    tree = patch.visit(ast.parse(original))
    assert patch.recovery_loops == 3, patch.recovery_loops
    ast.fix_missing_locations(tree)
    runtime = "_RECOVERY = None\n" + ast.unparse(tree) + "\n"
    if config.get("profile") == "paper_equations_v1":
        runtime += """
# Numerical adapters for the original SD3 VAE. The transformer remains float16.
def _paper_encode(self, image):
    with torch.no_grad():
        output = self.vae.encode(image.to(device=self.vae.device, dtype=self.vae.dtype))
        latent = output.latent_dist.mode()
    return ((latent - self.vae.config.shift_factor) * self.vae.config.scaling_factor).float()
def _paper_decode(self, latent):
    value = latent.to(device=self.vae.device, dtype=self.vae.dtype)
    value = value / self.vae.config.scaling_factor + self.vae.config.shift_factor
    return self.vae.decode(value, return_dict=False)[0]
_original_predict = StableDiffusion3Base.predict_vector
def _paper_predict(self, z, t, prompt_emb, pooled_emb):
    return _original_predict(self, z.to(dtype=self.dtype), t, prompt_emb, pooled_emb).float()
_original_initialize = StableDiffusion3Base.initialize_latent
def _paper_initialize(self, *args, **kwargs):
    return _original_initialize(self, *args, **kwargs).float()
StableDiffusion3Base.encode = _paper_encode
StableDiffusion3Base.decode = _paper_decode
StableDiffusion3Base.predict_vector = _paper_predict
StableDiffusion3Base.initialize_latent = _paper_initialize
from paper_hdps import PaperHDPS
__SOLVER__["hdps"] = type("SD3PaperHDPS", (PaperHDPS, SD3HDPS), {})
"""

    compile(runtime, str(destination), "exec")
    destination = Path(destination)
    if not destination.exists() or destination.read_text(encoding="utf-8") != runtime:
        temporary = destination.with_suffix(".tmp." + str(os.getpid()))
        temporary.write_text(runtime, encoding="utf-8")
        os.replace(temporary, destination)
    difference = "".join(difflib.unified_diff(
        original.splitlines(True), runtime.splitlines(True),
        fromfile="upstream/sd3_sampler.py", tofile="runtime_sampler.py"))
    Path(destination).with_suffix(".diff").write_text(difference, encoding="utf-8")
    return hashlib.sha256(original.encode()).hexdigest(), hashlib.sha256(runtime.encode()).hexdigest()
