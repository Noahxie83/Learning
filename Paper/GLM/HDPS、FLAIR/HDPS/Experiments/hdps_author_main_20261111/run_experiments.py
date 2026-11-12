#!/usr/bin/env python3
"""HDPS Table-1 campaign: shared observations, strict pairing, recoverable samples."""
import argparse
import csv
import gc
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import shutil
import sys
import time
import traceback
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
RESULT_CACHE = None
MULTI_WORKER = False
ACTIVE_MONITOR = None


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp." + str(os.getpid()))
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def stable_seed(*values):
    return int(hashlib.sha256("|".join(map(str, values)).encode()).hexdigest()[:8], 16)


def seed_all(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def datasets(config, limit):
    selected = []
    missing = []
    for dataset in config["datasets"]:
        directory = Path(dataset["path"])
        if not directory.is_absolute():
            directory = ROOT / directory
        files = sorted(p for p in directory.rglob("*")
                       if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"})
        if dataset.get("classes"):
            files = [p for p in files if p.relative_to(directory).parts[0] in dataset["classes"]]
        if len(files) != dataset["expected_count"]:
            missing.append({"dataset": dataset["name"], "expected": dataset["expected_count"],
                            "found": len(files), "path": str(directory)})
            continue  # Never silently treat a smaller dataset as its full split.
        captions = {}
        if dataset.get("caption_file"):
            for line in Path(dataset["caption_file"]).read_text().splitlines():
                name, text = line.split(":", 1)
                assert name.strip() not in captions
                captions[name.strip()] = "a high quality photo of " + text.strip()
            if set(p.name for p in files) != set(captions):
                raise RuntimeError("DAPE filenames do not match the DIV2K image manifest")
        items = []
        for path in files[:limit or None]:
            if captions:
                prompt = captions[path.name]
            elif dataset.get("classes"):
                prompt = "a photo of a closed face of a " + path.relative_to(directory).parts[0]
            else:
                prompt = dataset["prompt"]
            items.append({"path": str(path), "id": path.stem,
                          "relative_path": path.relative_to(directory).as_posix(),
                          "prompt": prompt})
        selected.append({**dataset, "items": items})
    return selected, missing


def aggregate(new_record=None, write=True):
    global RESULT_CACHE
    if RESULT_CACHE is None or MULTI_WORKER:
        RESULT_CACHE = {}
        for path in (ROOT / "results").glob("*/*/*/*.json"):
            record = json.loads(path.read_text())
            if record.get("complete"):
                key = (record["dataset"], record["task"], record["method"], record["sample"])
                RESULT_CACHE[key] = record
    if new_record is not None:
        key = (new_record["dataset"], new_record["task"], new_record["method"], new_record["sample"])
        RESULT_CACHE[key] = new_record
    if not write:
        return
    targets = {(x["dataset"], x["task"], x["method"]): x for x in
               json.loads((ROOT / "paper_table1_targets.json").read_text())}
    groups = defaultdict(list)
    for record in RESULT_CACHE.values():
        groups[(record["dataset"], record["task"], record["method"])].append(record)
    rows = []
    for key, records in sorted(groups.items()):
        row = dict(zip(["dataset", "task", "method"], key))
        row["count"] = len(records)
        for metric in ["psnr", "ssim", "lpips_code_vgg224_01", "lpips_standard_vgg768_m11",
                       "sampling_seconds", "peak_gpu_gib"]:
            values = [record[metric] for record in records
                      if metric != "sampling_seconds" or not record.get("resumed_from_step", 0)]
            row[metric] = float(np.mean(values)) if values else None
        row["timed_samples"] = sum(not record.get("resumed_from_step", 0) for record in records)
        target = targets[key]
        for name in ["psnr", "ssim"]:
            row["paper_" + name] = target[name]
            row["delta_" + name] = row[name] - target[name]
        row["paper_lpips"] = target["lpips"]
        row["delta_lpips_code"] = row["lpips_code_vgg224_01"] - target["lpips"]
        rows.append(row)
    if rows:
        temporary = ROOT / ("metrics_summary.csv.tmp." + str(os.getpid()))
        with temporary.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        os.replace(temporary, ROOT / "metrics_summary.csv")
    return rows


def main(args):
    global torch, np, MULTI_WORKER, ACTIVE_MONITOR
    MULTI_WORKER = args.num_shards > 1
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    for directory in ["logs", "checkpoints", "results", "manifests"]:
        (ROOT / directory).mkdir(exist_ok=True)
    selected, missing = datasets(config, args.limit)
    atomic_json(ROOT / "manifests/datasets.json", {"datasets": selected, "missing": missing})
    if missing:
        raise RuntimeError("Configured paper datasets missing: " + json.dumps(missing))
    if not selected:
        raise RuntimeError("No complete configured dataset is available")
    # All CUDA visibility is set in the launcher, before importing torch.
    if not os.environ.get("CUDA_VISIBLE_DEVICES"):
        raise RuntimeError("The monitor must provide a single CUDA_VISIBLE_DEVICES selection")
    import torch
    import numpy as np
    from PIL import Image
    from torchvision import transforms
    from torchvision.utils import save_image, make_grid
    from pytorch_msssim import ssim
    import lpips
    from munch import munchify
    from recovery import Recovery, InterruptedRun
    from prepare_runtime import prepare
    from monitoring import Monitor, effective_steps
    from diffusers.utils.logging import disable_progress_bar as disable_diffusers_bars
    from transformers.utils.logging import disable_progress_bar as disable_transformers_bars
    disable_diffusers_bars()
    disable_transformers_bars()

    torch.set_num_threads(config["cpu_threads"])
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    if torch.cuda.device_count() != 1:
        raise RuntimeError("Exactly one reviewed GPU must be visible to each worker")
    sys.path.insert(0, config["repo"])
    os.chdir(config["repo"])
    from functions.degradation import get_degradation
    upstream_hash, runtime_hash = prepare(config, ROOT / "runtime_sampler.py")
    driver_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    fingerprint = hashlib.sha256(
        (json.dumps(config, sort_keys=True) + upstream_hash + runtime_hash + driver_hash).encode()).hexdigest()
    specification = importlib.util.spec_from_file_location("hdps_campaign_runtime", ROOT / "runtime_sampler.py")
    runtime = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(runtime)
    original_tqdm = runtime.tqdm
    def silent_solver_progress(*positional, **keywords):
        keywords['disable'] = True
        return original_tqdm(*positional, **keywords)
    runtime.tqdm = silent_solver_progress
    atomic_json(ROOT / f"manifests/runtime_worker_{args.shard_rank}.json", {
        "upstream_sha256": upstream_hash, "runtime_sha256": runtime_hash,
        "driver_sha256": driver_hash,
        "fingerprint": fingerprint, "torch": torch.__version__,
        "visible_gpu": os.environ["CUDA_VISIBLE_DEVICES"], "pid": os.getpid()})
    total = sum(len(d["items"]) for d in selected) * len(config["tasks"]) * len(config["methods"])
    existing = [json.loads(p.read_text()) for p in (ROOT / "results").glob("*/*/*/*.json")]
    existing = [record for record in existing if record.get("fingerprint") == fingerprint and record.get("complete")]
    completed = len(existing)
    completed_outer = sum(record["outer_steps"] for record in existing)
    total_outer = sum(len(d["items"]) * sum(effective_steps(method, task["name"], config["nfe"])
                      for task in config["tasks"] for method in config["methods"]) for d in selected)
    partial_outer = 0
    for checkpoint in (ROOT / "checkpoints").glob("*.pt"):
        saved = torch.load(checkpoint, map_location="cpu", weights_only=False)
        parts = saved["job"].split("/")
        if len(parts) != 4:
            raise RuntimeError("Malformed checkpoint job")
        finished_path = ROOT / "results" / parts[0] / parts[1] / parts[2] / (parts[3]+".json")
        if finished_path.exists():
            continue
        data = next(d for d in selected if d["name"] == parts[0])
        item = next(x for x in data["items"] if x["id"] == parts[3])
        source_sha = hashlib.sha256(Path(item["path"]).read_bytes()).hexdigest()
        corruption_seed = stable_seed(config["seed"], parts[0], parts[1], parts[3])
        expected = hashlib.sha256((fingerprint+source_sha+item["prompt"]+str(corruption_seed)).encode()).hexdigest()
        if saved["fingerprint"] != expected:
            raise RuntimeError("Checkpoint protocol/input mismatch")
        partial_outer += saved["next_step"]
    status = {"task_id": config["run_id"], "status": "starting", "pid": os.getpid(),
              "logical_gpu": "cuda:0", "visible_gpu": os.environ.get("CUDA_VISIBLE_DEVICES"),
              "total_samples": total, "completed_samples": completed,
              "paper_full_target_samples": 42000, "missing_datasets": missing,
              "profile": config["profile"], "shard_rank": args.shard_rank,
              "num_shards": args.num_shards}

    status_path = ROOT / ("status.json" if args.shard_rank == 0 else f"status_worker_{args.shard_rank}.json")
    monitor = Monitor(status_path, config["run_id"], total_outer, completed_outer+partial_outer, status, atomic_json)
    ACTIVE_MONITOR = monitor

    def update(**changes):
        status.update(changes)
        if "completed_samples" in changes:
            status["sampling_step"] = 0
        status["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        monitor.update(max(monitor.actual, completed_outer+status.get("sampling_step",0)), **status)


    update(status="loading_models")
    metric = None
    transform = transforms.Compose([transforms.Resize(config["image_size"]),
                                     transforms.CenterCrop(config["image_size"]),
                                     transforms.ToTensor()])
    metric_transform = transforms.Compose([transforms.Resize((224, 224)),
                                           transforms.ToTensor()])
    job_index = -1
    source_hashes = {}
    for dataset in selected:
        update(status="loading_models", dataset=dataset["name"])
        print(f"DATASET {dataset['name']} images={len(dataset['items'])}", flush=True)
        base = runtime.get_solver("hdps")
        for encoder in [base.text_enc_1, base.text_enc_2, base.text_enc_3]:
            encoder.to("cuda")
        prompts = sorted(set([""] + [item["prompt"] for item in dataset["items"]]))
        embeddings = {}
        for index, prompt in enumerate(prompts):
            with torch.no_grad():
                embeddings[prompt] = [x.detach().cpu() for x in base.encode_prompt([prompt], 1)]
            update(status="encoding_prompts", prompts_done=index + 1, prompts_total=len(prompts))
            if index % 25 == 0:
                print(f"PROMPTS {index+1}/{len(prompts)}", flush=True)
        del base.text_enc_1, base.text_enc_2, base.text_enc_3
        del encoder  # Release the loop's last T5 reference as well as the attributes.
        torch.cuda.empty_cache()
        base.vae.to("cuda")
        base.transformer.to("cuda")
        solvers = {}
        for method in config["methods"]:
            solver = object.__new__(runtime.__SOLVER__[method])
            solver.__dict__.update(base.__dict__)
            solvers[method] = solver
        if metric is None:
            metric = lpips.LPIPS(net="vgg").to("cuda").eval()
            metric.requires_grad_(False)
        for task in config["tasks"]:
            operator_seed = stable_seed(config["seed"], dataset["name"], task["name"], "operator")
            seed_all(operator_seed)
            deg = munchify({"channels": 3, "image_size": config["image_size"],
                            "deg_scale": task["deg_scale"], "inpainting_config": [{
                                "mask_type": task.get("mask_type"), "mask_len_range": [384, 385],
                                "mask_prob_range": [0.3, 0.7], "image_size": config["image_size"]}]})
            operator = get_degradation(task["name"], deg, torch.device("cuda"))
            for item in dataset["items"]:
                path = Path(item["path"])
                source_hashes.setdefault(str(path), hashlib.sha256(path.read_bytes()).hexdigest())
                image = transform(Image.open(path).convert("RGB")).unsqueeze(0).to("cuda")
                image = image * 2 - 1
                corruption_seed = stable_seed(config["seed"], dataset["name"], task["name"], item["id"])
                for method in config["methods"]:
                    job_index += 1
                    if job_index % args.num_shards != args.shard_rank:
                        continue
                    output = ROOT / "results" / dataset["name"] / task["name"] / method / (item["id"] + ".png")
                    record_path = output.with_suffix(".json")
                    if record_path.exists():
                        record = json.loads(record_path.read_text())
                        if record.get("fingerprint") != fingerprint or record.get("source_sha256") != source_hashes[str(path)]:
                            raise RuntimeError(f"Existing result has a different protocol/input: {record_path}")
                        if output.is_file() and record.get("complete") and hashlib.sha256(output.read_bytes()).hexdigest() == record.get("output_sha256"):
                            continue
                    if shutil.disk_usage(ROOT).free < config["minimum_free_disk_gib"] * 1024**3:
                        update(status="paused_disk_space")
                        print("PAUSED: free disk space below configured floor", flush=True)
                        monitor.close()
                        return
                    seed_all(corruption_seed)
                    observation = operator.A(image)
                    observation = observation + config["noise_std"] * torch.randn_like(observation)
                    key = "/".join([dataset["name"], task["name"], method, item["id"]])
                    update(status="running", job=key, method=method, task=task["name"], sample=item["id"],
                           sampling_step=0, sampling_steps=config["nfe"])
                    def progress(step):
                        update(sampling_step=step)
                        if step % config["checkpoint_every"] == 0:
                            print(f"STEP job={key} step={step}/{config['nfe']}", flush=True)
                    recovery_fingerprint = hashlib.sha256(
                        (fingerprint + source_hashes[str(path)] + item["prompt"] + str(corruption_seed)).encode()).hexdigest()
                    recovery = Recovery(ROOT / "checkpoints" / (hashlib.sha256(key.encode()).hexdigest() + ".pt"),
                                        key, recovery_fingerprint, config["checkpoint_every"], progress)
                    recovery.install_signals()
                    runtime._RECOVERY = recovery
                    solver = solvers[method]
                    step_size = (12.0 if "sr" in task["name"] else 0.1) if method == "flair" else 15.0
                    prompt_embedding = [x.to("cuda") for x in embeddings[item["prompt"]]]
                    null_embedding = [x.to("cuda") for x in embeddings[""]]
                    torch.cuda.reset_peak_memory_stats()
                    started = time.monotonic()
                    try:
                        prediction = solver.sample(
                            measurement=observation, operator=operator, task=task["name"],
                            prompts=item["prompt"], NFE=config["nfe"],
                            img_shape=(config["image_size"], config["image_size"]),
                            cfg_scale=config["cfg_scale"], step_size=step_size,
                            prompt_emb=prompt_embedding, null_emb=null_embedding,
                            mask_type=task.get("mask_type"))
                    except InterruptedRun:
                        aggregate()
                        update(status="paused", checkpoint=str(recovery.path))
                        print("PAUSED: recovery checkpoint saved", flush=True)
                        monitor.close()
                        return
                    expected_steps = effective_steps(method, task["name"], config["nfe"])
                    if status["sampling_step"] != expected_steps:
                        raise RuntimeError("Incomplete outer sampling budget")
                    torch.cuda.synchronize()
                    sampling_seconds = time.monotonic() - started
                    peak_gpu = torch.cuda.max_memory_allocated() / 1024**3
                    if not torch.isfinite(prediction).all():
                        raise RuntimeError(f"Non-finite prediction: {key}")
                    output.parent.mkdir(parents=True, exist_ok=True)
                    temporary = output.with_name(output.stem + ".tmp.png")
                    save_image(prediction.detach(), temporary, normalize=True)
                    os.replace(temporary, output)
                    # Match upstream eval.py: PNG quantization, VGG224 inputs in [0,1].
                    restored = transforms.ToTensor()(Image.open(output).convert("RGB")).unsqueeze(0).to("cuda")
                    reference = make_grid(image.detach(), normalize=True).unsqueeze(0)
                    reference = (reference * 255 + 0.5).clamp(0, 255).to(torch.uint8).float() / 255
                    with torch.no_grad():
                        mse = torch.mean((restored - reference) ** 2).item()
                        psnr = -10 * np.log10(max(mse, 1e-16))
                        ssim_value = ssim(restored * 255, reference * 255, data_range=255).item()
                        reference_pil = Image.fromarray(
                            (reference[0].permute(1, 2, 0).cpu().numpy() * 255).round().astype(np.uint8))
                        small_ref = metric_transform(reference_pil).unsqueeze(0).to("cuda")
                        small_out = metric_transform(Image.open(output).convert("RGB")).unsqueeze(0).to("cuda")
                        legacy = metric(small_ref, small_out).item()
                        standard = metric(reference * 2 - 1, restored * 2 - 1).item()
                    record = {
                        "complete": True, "dataset": dataset["name"], "task": task["name"],
                        "method": method, "sample": item["id"], "source": str(path),
                        "source_sha256": source_hashes[str(path)], "corruption_seed": corruption_seed,
                        "operator_seed": operator_seed,
                        "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                        "prompt": item["prompt"], "fingerprint": fingerprint,
                        "driver_sha256": driver_hash, "resumed_from_step": recovery.next_step,
                        "psnr": float(psnr), "ssim": ssim_value,
                        "lpips_code_vgg224_01": legacy, "lpips_standard_vgg768_m11": standard,
                        "sampling_seconds": sampling_seconds, "peak_gpu_gib": peak_gpu,
                        "outer_steps": expected_steps}
                    if key == "FFHQ/deblur_gauss/hdps/00000":
                        expected_output = "82c7460d5d5f19c5bfb68d997a5afc891108acb2ab87f4c5ad18e36c41b7dde1"
                        if record["output_sha256"] != expected_output:
                            raise RuntimeError("Public algorithm first-result hash differs from the validated audit")
                    atomic_json(record_path, record)
                    aggregate(record, write=False)
                    completed += 1
                    completed_outer += expected_steps
                    update(completed_samples=completed, last_metrics=record,
                           checkpoint=str(recovery.path))
                    print(f"RESULT {key} psnr={psnr:.5f} ssim={ssim_value:.6f} "
                          f"lpips_code={legacy:.6f} lpips_standard={standard:.6f} "
                          f"seconds={sampling_seconds:.2f} completed={completed}/{total}", flush=True)
                    if completed == 1 or completed % 10 == 0:
                        aggregate()
                    del prediction, restored, reference, observation
                    # Result+hash is the durable completion record; discard this job's transient checkpoint.
                    if recovery.path.is_file():
                        assert recovery.path.resolve().parent == (ROOT / "checkpoints").resolve()
                        recovery.path.unlink()
                    if recovery.stop_requested:
                        aggregate()
                        update(status="paused")
                        print("PAUSED: current result committed", flush=True)
                        monitor.close()
                        return
                    torch.cuda.empty_cache()
        del base, solvers, embeddings, solver
        gc.collect()
        torch.cuda.empty_cache()
    aggregate()
    update(status="partial_missing_assets" if missing else "completed")
    print("CAMPAIGN FINISHED", json.dumps(status), flush=True)
    monitor.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Explicit pilot subset size per dataset; 0 runs configured full splits.")
    parser.add_argument("--num-shards", type=int, default=1)
    parser.add_argument("--shard-rank", type=int, default=0)
    parser.add_argument("--allow-other-gpu", action="store_true", help="Only use after explicitly selecting another GPU for an additional worker.")
    args = parser.parse_args()
    assert args.num_shards > 0 and 0 <= args.shard_rank < args.num_shards
    try:
        main(args)
    except Exception as error:
        traceback.print_exc()
        if ACTIVE_MONITOR is not None:
            ACTIVE_MONITOR.update(ACTIVE_MONITOR.actual, status="failed", error=str(error))
            ACTIVE_MONITOR.close()
        else:
            atomic_json(ROOT / "status.json", {"status": "failed", "pid": os.getpid(),
                                              "error": str(error), "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
        raise
