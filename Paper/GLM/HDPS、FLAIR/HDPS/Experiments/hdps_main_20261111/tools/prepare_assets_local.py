"""Download public prerequisites; extract only official AFHQ validation cats/dogs."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path, PurePosixPath
import urllib.request
import zipfile

CACHE = Path(r"C:\Users\noahx\.codex\visualizations\2026\11\04\01a1a703-ab56-79d2-9ef9-ab57d2c63a91\hdps_assets_20261111")
CACHE.mkdir(exist_ok=True)
ASSETS = {
    "vgg16-397923af.pth": ("https://download.pytorch.org/models/vgg16-397923af.pth", 553433881),
    "afhq.zip": ("https://dl.dropboxusercontent.com/s/t9l9o3vsx2jai3z/afhq.zip", 729484677),
}


def download(item):
    name, (url, expected) = item
    target = CACHE / name
    if not target.is_file() or target.stat().st_size != expected:
        temporary = target.with_suffix(target.suffix + ".part")
        with urllib.request.urlopen(url, timeout=60) as response, temporary.open("wb") as output:
            while block := response.read(4 * 1024**2):
                output.write(block)
        assert temporary.stat().st_size == expected
        temporary.replace(target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if name.startswith("vgg16"):
        assert digest.startswith("397923af")
    print(json.dumps({"downloaded": str(target), "sha256": digest, "bytes": expected}), flush=True)
    return name, digest


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as pool:
        hashes = dict(pool.map(download, ASSETS.items()))
    output = CACHE / "afhq_validation"
    counts = {"cat": 0, "dog": 0}
    with zipfile.ZipFile(CACHE / "afhq.zip") as archive:
        for item in archive.infolist():
            path = PurePosixPath(item.filename)
            if item.is_dir() or len(path.parts) < 4:
                continue
            if path.parts[:3] not in [("afhq", "val", "cat"), ("afhq", "val", "dog")]:
                continue
            assert ".." not in path.parts and not path.is_absolute()
            relative = Path(*path.parts[2:])
            destination = output / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            data = archive.read(item)  # ZIP CRC validated by zipfile.
            if destination.exists():
                assert destination.read_bytes() == data
            else:
                destination.write_bytes(data)
            counts[path.parts[2]] += 1
    assert counts == {"cat": 500, "dog": 500}, counts
    (CACHE / "sources.json").write_text(json.dumps({
        "assets": ASSETS, "sha256": hashes, "afhq_validation": counts,
        "afhq_publisher": "https://github.com/clovaai/stargan-v2",
        "afhq_license": "CC BY-NC 4.0"}, indent=2), encoding="utf-8")
    print(json.dumps({"afhq_ready": str(output), "counts": counts}), flush=True)
