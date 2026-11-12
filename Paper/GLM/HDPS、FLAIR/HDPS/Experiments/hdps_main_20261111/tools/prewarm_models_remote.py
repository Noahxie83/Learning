"""Read model shards sequentially into the OS page cache; no model copies or edits."""
from pathlib import Path
import time

root = Path("/data2/cy/caoyi/huggingface/hub/models--stabilityai--stable-diffusion-3-medium-diffusers/snapshots/ea42f8cef0f178587cf766dc8129abd379c90671")
files = sorted((root / "text_encoder_3").glob("*.safetensors"))
files += sorted((root / "transformer").glob("*.safetensors"))
buffer = bytearray(16 * 1024**2)
for path in files:
    start = time.monotonic()
    count = 0
    with path.open("rb") as handle:
        while length := handle.readinto(buffer):
            count += length
    print(path.name, count, "bytes", round(time.monotonic() - start, 1), "seconds", flush=True)
