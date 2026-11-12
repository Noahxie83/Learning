"""HDPS Algorithm 1 and Eqs. 6--12 of the supplied PDF.

The paper omits eta_x/eta_z; the fixed, untuned choices are in config.json.
This module never reads ground truth or evaluation scores.
"""
import math
import torch


def posterior_gradient(x, anchor, operator, measurement, sigma, noise_std):
    """Eq. 8: autodiff implements the actual A transpose, including boundaries."""
    with torch.enable_grad():
        variable = x.detach().requires_grad_(True)
        energy = (operator.A(variable) - measurement).square().sum() / (2 * noise_std**2)
        likelihood_gradient = torch.autograd.grad(energy, variable)[0]
    tau_squared = sigma**2 / (1 + sigma**2)
    return -likelihood_gradient + (anchor - x) / tau_squared


def pixel_correction(anchor, operator, measurement, sigma, noise_std, steps, eta):
    x = anchor.detach().float().clone()
    for _ in range(steps):
        gradient = posterior_gradient(x, anchor, operator, measurement, sigma, noise_std)
        x = (x + eta * gradient + math.sqrt(2 * eta) * torch.randn_like(x)).detach()
        if not torch.isfinite(x).all():
            raise RuntimeError("Non-finite Eq. 8 pixel correction")
    return x  # Eq. 8 has no clipping/projection inside its Langevin chain.


def align(decoder, initial, target, steps, eta, max_backtracks=12):
    """Eq. 9 squared L2 gradient descent; backtracking uses only its objective."""
    z = initial.detach().float().clone()
    first = None
    final = None
    accepted_etas = []
    for _ in range(steps):
        with torch.enable_grad():
            variable = z.detach().requires_grad_(True)
            objective = (decoder(variable).float() - target).square().sum()
            gradient = torch.autograd.grad(objective, variable)[0]
        current = float(objective.detach())
        if first is None:
            first = current
        if not torch.isfinite(gradient).all():
            raise RuntimeError("Non-finite Eq. 9 gradient")
        trial_eta = eta
        for attempt in range(max_backtracks + 1):
            proposal = z - trial_eta * gradient
            with torch.no_grad():
                proposal_objective = float((decoder(proposal).float() - target).square().sum())
            # Armijo descent; no reference image or restoration metric is used.
            if math.isfinite(proposal_objective) and proposal_objective <= current - 1e-4 * trial_eta * float(gradient.square().sum()):
                z, final = proposal.detach(), proposal_objective
                accepted_etas.append(trial_eta)
                break
            trial_eta *= 0.5
        else:
            raise RuntimeError("Eq. 9 line search failed; stop rather than accept an unstable alignment")
    return z, {"alignment_initial_sse": first, "alignment_final_sse": final,
               "alignment_eta_min": min(accepted_etas), "alignment_eta_max": max(accepted_etas)}


class PaperHDPS:
    def sample(self, measurement, operator, task, prompts, NFE, img_shape,
               cfg_scale=2.0, prompt_emb=None, null_emb=None, **kwargs):
        config = self.paper_config
        options = config["paper_parameters"]["hdps"]
        device = self.device
        recovery = self.paper_recovery
        H, W = img_shape
        # Eq. 12. Use the exposed truncated SVD pseudoinverse where available.
        with torch.no_grad():
            source = operator.A_pinv(measurement) if hasattr(operator, "A_pinv") else operator.At(measurement)
            source = source.view(1, 3, H, W)
            encoded = self.encode(source).float()
            z0y = encoded.clone()
            t0 = options["initialization_ratio"]
            z = t0 * self.initialize_latent(img_shape, 1).float() + (1 - t0) * encoded
        # Algorithm 1: uniform reverse time grid beginning at exactly t0=0.8.
        sigmas = torch.linspace(t0, 0, NFE + 1, device=device, dtype=torch.float32)
        variables = {"z": z, "z0y": z0y}
        resume = recovery.restore(variables)
        z, z0y = variables["z"], variables["z0y"]
        trace = []
        for i in range(resume, NFE):
            sigma = float(sigmas[i])
            sigma_next = float(sigmas[i + 1])
            timestep = (sigmas[i] * self.scheduler.config.num_train_timesteps).expand(1)
            with torch.no_grad():
                conditional = self.predict_vector(z, timestep, *prompt_emb).float()
                unconditional = self.predict_vector(z, timestep, *null_emb).float()
                # Eq. 6 uses lambda=2, equivalent to diffusers guidance_scale=3.
                velocity = (1 + cfg_scale) * conditional - cfg_scale * unconditional
                clean = z - sigma * velocity
                endpoint = z + (1 - sigma) * velocity  # Eq. 3 linear endpoint convention.
                anchor = self.decode(clean).float()
            eta_x = options["eta_x"][task]
            corrected = pixel_correction(anchor, operator, measurement, sigma,
                                         config["noise_std"], options["pixel_steps"], eta_x)
            z0y, diagnostic = align(self.decode, clean, corrected,
                                    options["alignment_steps"], options["eta_z"])
            with torch.no_grad():
                alpha = 1 - sigma
                perturbed_endpoint = alpha * endpoint + math.sqrt(1 - alpha**2) * torch.randn_like(endpoint)
                z = (1 - sigma_next) * z0y + sigma_next * perturbed_endpoint
            trace.append({"step": i + 1, "sigma": sigma, "eta_x": eta_x,
                          "pixel_steps": options["pixel_steps"],
                          "alignment_steps": options["alignment_steps"], **diagnostic})
            if not torch.isfinite(z).all():
                raise RuntimeError("Non-finite Eq. 11 state")
            recovery.save(i + 1, {"z": z, "z0y": z0y})
        self.last_diagnostics = trace
        with torch.no_grad():
            return self.decode(z0y)
