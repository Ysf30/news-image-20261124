#!/usr/bin/env python3
"""Entrypoint for news-image-20261124.

Renders the front page fresh with build_image.py and places the finished
PNG at the grader's output path. Stdlib only, no network, deterministic.
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def png_size(blob):
    """Return (width, height) from a PNG's IHDR chunk, or None."""
    if len(blob) < 33 or blob[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if blob[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def checked_copy(src, dst):
    """Copy src to dst, verifying magic bytes, size and a hash round-trip."""
    blob = src.read_bytes()
    dims = png_size(blob)
    if dims is None:
        raise SystemExit("entry image is not a valid PNG")
    if dims != (1024, 1024):
        raise SystemExit(f"unexpected image size {dims}, want (1024, 1024)")
    if len(blob) > 1048576:
        raise SystemExit(f"image too large: {len(blob)} bytes")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    again = dst.read_bytes()
    if hashlib.sha256(again).hexdigest() != hashlib.sha256(blob).hexdigest():
        raise SystemExit("output failed its read-back hash check")
    if png_size(again) != (1024, 1024):
        raise SystemExit("output failed its dimension re-check")
    return len(blob)


def main():
    sys.path.insert(0, str(HERE))
    import build_image

    made = build_image.build()
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
    size = checked_copy(made, target)
    print(f"entry.png: {size} bytes, 1024x1024, sha256 "
          f"{hashlib.sha256(target.read_bytes()).hexdigest()[:16]}...")


if __name__ == "__main__":
    main()
