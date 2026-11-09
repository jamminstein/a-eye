#!/usr/bin/env python3
"""Rebuild every clip on the site from the masters at the look in look.json.

    kling/recompress.py                       # the look in kling/look.json
    kling/recompress.py --height 480 --crf 34 --maxrate 600k
    kling/recompress.py --only eye-07,classic

The look is the dial for "how perfect": lower resolution is upscaled by the browser,
which softens it the way a real camera and a real re-upload do, and a lower bitrate
smooths away the over-sharp micro-detail that makes generated footage read as generated.
The film grain is added in the browser on top, so it is never baked in here.

Always encodes from kling/masters/ (the clips as they were at 1080p, kept locally, not
in git), never from clips/, so changing the look never stacks one lossy pass on another.
Make the masters once from the clips in a given commit:
    mkdir -p kling/masters && git show <commit>:clips/eye-07.mp4 > kling/masters/eye-07.mp4
    cp eye.mp4 kling/masters/classic.mp4          # the original, before its first recompress
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import ingest  # noqa: E402  (shares the manifest writer)

MASTERS = HERE / "masters"
LOOK = json.loads((HERE / "look.json").read_text())


def sh(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, stdin=subprocess.DEVNULL)


def encode(master, dst, height, crf, maxrate):
    br = int(maxrate.rstrip("k"))
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(master),
        "-vf", f"scale=-2:'min({height},ih)':flags=bicubic", "-an",
        "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
        "-maxrate", maxrate, "-bufsize", f"{br * 2}k",
        "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)])


def poster(video, dst):
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video),
        "-frames:v", "1", "-q:v", "5", str(dst)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--height", type=int, default=LOOK["height"])
    ap.add_argument("--crf", type=int, default=LOOK["crf"])
    ap.add_argument("--maxrate", default=LOOK["maxrate"])
    ap.add_argument("--max-mb", type=float, default=LOOK["max_mb"], help="encode harder above this size")
    ap.add_argument("--only", help="comma list of ids, e.g. eye-07,eye-09b,classic")
    args = ap.parse_args()

    masters = sorted(MASTERS.glob("*.mp4"))
    if not masters:
        raise SystemExit(f"no masters in {MASTERS}")
    only = set(args.only.split(",")) if args.only else None
    before = after = 0
    for m in masters:
        cid = m.stem
        if only and cid not in only:
            continue
        # the original clip lives at the site root; its poster is clips/classic.jpg because
        # poster.jpg is the sharp link-preview image and must stay as it is
        out = ROOT / "eye.mp4" if cid == "classic" else ingest.CLIPS / f"{cid}.mp4"
        post = ingest.CLIPS / f"{cid}.jpg"
        crf = args.crf
        tmp = out.with_suffix(".tmp.mp4")
        for _ in range(4):
            encode(m, tmp, args.height, crf, args.maxrate)
            if tmp.stat().st_size / 1e6 <= args.max_mb:
                break
            crf += 2
        tmp.replace(out)
        poster(out, post)
        before += m.stat().st_size
        after += out.stat().st_size
        print(f"{cid:10s} {m.stat().st_size / 1e6:5.1f} MB -> {out.stat().st_size / 1e6:4.1f} MB  (crf {crf})", flush=True)
    ingest.write_manifest()
    print(f"\n{before / 1e6:.0f} MB -> {after / 1e6:.0f} MB at {args.height}p, crf {args.crf}, max {args.maxrate}")


if __name__ == "__main__":
    main()
