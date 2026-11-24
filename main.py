#!/usr/bin/env python3
"""news-image-20261124 entrypoint.

Copies the pre-rendered front page (entry.png, drawn by
build_image.py from the day's researched news) to the grader's
output directory. Standard library only, no network, deterministic:
the same bytes every run.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py

Exit code 0 means the copy landed byte-identical; any other code
means the entry is invalid and must not be submitted.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = SRC.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    # IHDR: width and height are big-endian uint32 at bytes 16..24.
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > 1024 or height > 1024:
        print(f"entry.png too large: {width}x{height}", file=sys.stderr)
        return 1
    if len(data) > 1_048_576:
        print(f"entry.png too large: {len(data)} bytes", file=sys.stderr)
        return 1
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    back = dest.read_bytes()
    if hashlib.sha256(back).hexdigest() != hashlib.sha256(data).hexdigest():
        print("read-back mismatch", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(back)} bytes, "
          f"sha256 {hashlib.sha256(back).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
