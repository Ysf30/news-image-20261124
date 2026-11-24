#!/usr/bin/env python3
"""news-image-20261124 entrypoint.

Copies the pre-rendered front page (entry.png, drawn by build_image.py
from the day's researched news) to the grader's output directory.
Standard library only, no network, deterministic: the same bytes every run.

Why a copy, not a render: the grader runs `python3 -P -s /bot/main.py`
in a pinned stock-python image with no Pillow, on a read-only /bot.
Rendering at grade time exits 1 there (no PIL, and nowhere writable to
save into). Copying the committed entry.png avoids both.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def png_size(blob):
    """Return (width, height) from a PNG's IHDR chunk, or None."""
    if len(blob) < 33 or blob[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if blob[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def main():
    # The grader sets MAKEFUN_OUTPUT_DIR=/output (empty, writable).
    # Local runs default there too; pass MAKEFUN_OUTPUT_DIR=out to test.
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    blob = SRC.read_bytes()
    dims = png_size(blob)
    if dims is None:
        print("entry.png is not a valid PNG", file=sys.stderr)
        return 1
    if dims != (1024, 1024):
        print(f"unexpected image size {dims}, want (1024, 1024)", file=sys.stderr)
        return 1
    if len(blob) > 1048576:
        print(f"image too large: {len(blob)} bytes", file=sys.stderr)
        return 1
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    again = dest.read_bytes()
    if hashlib.sha256(again).hexdigest() != hashlib.sha256(blob).hexdigest():
        print("output failed its read-back hash check", file=sys.stderr)
        return 1
    if png_size(again) != (1024, 1024):
        print("output failed its dimension re-check", file=sys.stderr)
        return 1
    print(f"entry.png: {len(blob)} bytes, 1024x1024, sha256 "
          f"{hashlib.sha256(blob).hexdigest()[:16]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
