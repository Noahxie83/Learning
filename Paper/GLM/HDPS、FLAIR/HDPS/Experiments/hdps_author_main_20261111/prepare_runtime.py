"""Adapt paths and recovery hooks; verify all three released solvers unchanged."""
import ast
import difflib
import hashlib
import os
from pathlib import Path


class RuntimePatch(ast.NodeTransformer):
    def __init__(self, config):
        assert config['profile'] == 'author_release'
        self.config = config
        self.class_name = None
        self.function_name = None
        self.recovery_loops = 0

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
        return None if node.module == 'piq' else node

    def visit_Constant(self, node):
        replacements = {
            'stabilityai/stable-diffusion-3-medium-diffusers': self.config['model'],
            'pretrained_models/taesd3': self.config['tiny_vae'],
            '../../FLAIR/FLAIR-main/LCFM/SD3_loss_v_MSE_DIV2k_neg_prompt.npy': self.config['flair_regularizer'],
        }
        if isinstance(node.value, str) and node.value in replacements:
            node.value = replacements[node.value]
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        names = [ast.unparse(n) for n in node.targets]
        if 'self.lpips_loss' in names:
            node.value = ast.Constant(None)  # Unused by these samplers.
        if names == ['pipe.vae']:
            return [node, *ast.parse('pipe.vae.register_to_config(shift_factor=0.0)\n'
                                    'pipe.vae.requires_grad_(False)\npipe.vae.eval()').body]
        return node

    def visit_For(self, node):
        self.generic_visit(node)
        states = {'SD3HDPS': ['z', 'z0y'], 'SD3FlowDPS': ['z'], 'SD3FLAIR': ['z0y', 'z1t']}
        if self.class_name not in states or self.function_name != 'sample' or ast.unparse(node.iter) != 'enumerate(pbar)':
            return node
        names = states[self.class_name]
        values = '{' + ', '.join(repr(n) + ': ' + n for n in names) + '}'
        optimizers = '(optimizer_x, optimizer_z)' if self.class_name == 'SD3FLAIR' else '()'
        before = ast.parse('_resume_variables = ' + values + '\n'
                           '_resume_step = _RECOVERY.restore(_resume_variables, ' + optimizers + ')\n'
                           + '\n'.join(n + ' = _resume_variables[' + repr(n) + ']' for n in names)).body
        node.body = ast.parse('if i < _resume_step:\n    continue').body + node.body
        node.body += ast.parse('_RECOVERY.save(i + 1, ' + values + ', ' + optimizers + ')').body
        self.recovery_loops += 1
        return before + [node]


class StripObserver(ast.NodeTransformer):
    def visit_Assign(self, node):
        if any(isinstance(t, ast.Name) and t.id in ['_resume_variables', '_resume_step'] for t in node.targets):
            return None
        if isinstance(node.value, ast.Subscript) and isinstance(node.value.value, ast.Name) and node.value.value.id == '_resume_variables':
            return None
        return self.generic_visit(node)

    def visit_If(self, node):
        return None if ast.unparse(node.test) == 'i < _resume_step' else self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call) and ast.unparse(node.value.func) == '_RECOVERY.save':
            return None
        return self.generic_visit(node)


def prepare(config, destination):
    original = (Path(config['repo'])/'sd3_sampler.py').read_text(encoding='utf-8')
    assert hashlib.sha256(original.encode()).hexdigest() == 'f8b709b49b7d8f3ec1904badade3510359f3ecf03bdf16522c4d32b1ae025992'
    patch = RuntimePatch(config)
    tree = patch.visit(ast.parse(original))
    assert patch.recovery_loops == 3
    ast.fix_missing_locations(tree)
    # All solver methods must match upstream after removing the observer hooks.
    for name in ['SD3HDPS', 'SD3FlowDPS', 'SD3FLAIR']:
        reference = next(n for n in ast.parse(original).body if isinstance(n, ast.ClassDef) and n.name == name)
        adapted = next(n for n in StripObserver().visit(ast.parse(ast.unparse(tree))).body if isinstance(n, ast.ClassDef) and n.name == name)
        for value in ast.walk(adapted):
            if isinstance(value, ast.Constant) and value.value == config['flair_regularizer']:
                value.value = '../../FLAIR/FLAIR-main/LCFM/SD3_loss_v_MSE_DIV2k_neg_prompt.npy'
        assert ast.dump(reference, include_attributes=False) == ast.dump(adapted, include_attributes=False), name
    runtime = '_RECOVERY = None\n' + ast.unparse(tree) + '\n'
    compile(runtime, str(destination), 'exec')
    destination = Path(destination)
    temporary = destination.with_suffix('.tmp.' + str(os.getpid()))
    temporary.write_text(runtime, encoding='utf-8')
    os.replace(temporary, destination)
    destination.with_suffix('.diff').write_text(''.join(difflib.unified_diff(
        original.splitlines(True), runtime.splitlines(True), fromfile='upstream', tofile='runtime')), encoding='utf-8')
    return hashlib.sha256(original.encode()).hexdigest(), hashlib.sha256(runtime.encode()).hexdigest()
