#!/usr/bin/env python3
"""Turn the clips you made in Kling into site assets.

    kling/ingest.py                   # everything new in kling/raw/
    kling/ingest.py ~/Downloads/kling # or another folder
    kling/ingest.py --rebuild-manifest

For each clip:
  1. find which of the 55 frames it came from (by "eye-07" in the file name if
     there is one, otherwise by comparing its first frame with every frame, so
     the names Kling gives the downloads do not matter);
  2. grade it to black and white and ping-pong it (forward, then reverse), the
     same loop trick as tools/pingpong.sh: no seam, no crossfade;
  3. encode clips/eye-NN.mp4 (H.264, faststart, 1080p max, a few MB) and a
     poster clips/eye-NN.jpg (its first frame);
  4. rewrite the clip list inside index.html so the page can pick one.

Files whose names start with _ or . are ignored: put a _ in front of a take you do not want.

Standard library + ffmpeg. Safe to re-run: clips that are already in clips/ are
skipped (--force replaces them).
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import specs  # noqa: E402

CLIPS = ROOT / "clips"
FRAMES = HERE / "frames"
INDEX = ROOT / "index.html"
GRADE = "hue=s=0"  # black and white, same as the original (grain is added in the browser)
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm"}
W, H = 32, 18


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def thumb(path, video):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)]
    if video:
        cmd += ["-frames:v", "1"]
    cmd += ["-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"]
    data = sh(cmd).stdout
    if len(data) != W * H:
        raise RuntimeError(f"unexpected thumbnail size for {path}")
    return data


def mad(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


_frame_thumbs = {}


def frame_thumbs():
    if not _frame_thumbs:
        for i in range(len(specs.SPECS)):
            p = FRAMES / f"{specs.ident(i)}.jpg"
            if p.exists():
                _frame_thumbs[specs.ident(i)] = thumb(p, video=False)
    return _frame_thumbs


def match(path):
    """Return (id, how) or (None, reason)."""
    m = re.search(r"eye[-_ ]?(\d{1,2})", path.stem, re.I)
    if m:
        n = int(m.group(1))
        if 1 <= n <= len(specs.SPECS):
            return specs.ident(n - 1), "name"
    t = thumb(path, video=True)
    scores = sorted((mad(t, ft), ident) for ident, ft in frame_thumbs().items())
    if not scores:
        return None, "no frames in kling/frames/"
    best, second = scores[0], scores[1] if len(scores) > 1 else (999, "")
    if best[0] <= 22 and second[0] >= best[0] * 1.4:
        return best[1], f"first frame (diff {best[0]:.1f} vs next {second[0]:.1f})"
    return None, f"ambiguous (best {best[1]} {best[0]:.1f}, next {second[1]} {second[0]:.1f}); put the eye number in the file name, e.g. eye-07.mp4"


def probe(path):
    out = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
              "-show_entries", "stream=nb_read_frames,width,height,r_frame_rate",
              "-of", "json", str(path)]).stdout
    s = json.loads(out)["streams"][0]
    return int(s["nb_read_frames"]), int(s["width"]), int(s["height"]), s["r_frame_rate"]


def encode(src, dst, n, crf, maxrate):
    last = n - 2
    vf = (f"{GRADE},scale='min(1920,iw)':'min(1080,ih)':force_original_aspect_ratio=decrease:flags=lanczos,"
          f"scale=trunc(iw/2)*2:trunc(ih/2)*2,split[a][b];"
          f"[b]reverse,select='between(n,1,{last})',setpts=N/FRAME_RATE/TB[r];"
          f"[a][r]concat=n=2:v=1:a=0[v]")
    br = int(maxrate.rstrip("k"))
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
        "-filter_complex", vf, "-map", "[v]", "-an",
        "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
        "-maxrate", maxrate, "-bufsize", f"{br * 2}k",
        "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)])


def write_manifest():
    ids = sorted(p.stem for p in CLIPS.glob("eye-*.mp4") if (CLIPS / f"{p.stem}.jpg").exists())
    block = "/*clips*/" + json.dumps(["classic"] + ids) + "/*end*/"
    html = INDEX.read_text()
    new, k = re.subn(r"/\*clips\*/.*?/\*end\*/", lambda _m: block, html, flags=re.S)
    if k != 1:
        raise SystemExit("could not find the /*clips*/ ... /*end*/ marker in index.html")
    if new != html:
        INDEX.write_text(new)
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", nargs="?", default=str(HERE / "raw"))
    ap.add_argument("--force", action="store_true", help="replace clips already in clips/")
    ap.add_argument("--crf", type=int, default=24)
    ap.add_argument("--maxrate", default="3500k")
    ap.add_argument("--max-mb", type=float, default=7.0, help="re-encode harder above this size")
    ap.add_argument("--rebuild-manifest", action="store_true")
    ap.add_argument("--dry", action="store_true", help="only show what would be matched")
    args = ap.parse_args()

    CLIPS.mkdir(exist_ok=True)
    if args.rebuild_manifest:
        print(f"manifest: classic + {len(write_manifest())} clips")
        return

    raw = Path(args.raw).expanduser()
    files = sorted(p for p in raw.glob("*")
                   if p.suffix.lower() in VIDEO_EXT and not p.name.startswith(("_", ".")))
    if not files:
        raise SystemExit(f"no videos in {raw}")

    done, skipped, unmatched = [], [], []
    claimed = {}
    for f in files:
        ident, how = match(f)
        if not ident:
            unmatched.append((f.name, how))
            print(f"?  {f.name}: {how}")
            continue
        if ident in claimed:
            skipped.append((f.name, f"second take of {ident} (first: {claimed[ident]})"))
            print(f"=  {f.name}: second take of {ident}, skipped (rename one if you prefer it)")
            continue
        claimed[ident] = f.name
        out = CLIPS / f"{ident}.mp4"
        if out.exists() and not args.force:
            print(f"=  {f.name} -> {ident}: already in clips/, skipped")
            continue
        print(f"-> {f.name} = {ident}  [{how}]", flush=True)
        if args.dry:
            continue
        t0 = time.time()
        n, w, h, fps = probe(f)
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td) / "out.mp4"
            crf = args.crf
            for _ in range(4):
                encode(f, tmp, n, crf, args.maxrate)
                mb = tmp.stat().st_size / 1e6
                if mb <= args.max_mb:
                    break
                crf += 3
            sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp),
                "-frames:v", "1", "-q:v", "5", str(Path(td) / "p.jpg")])
            tmp.replace(out)
            (Path(td) / "p.jpg").replace(CLIPS / f"{ident}.jpg")
        done.append(ident)
        print(f"   {w}x{h} {n} frames @ {fps} -> {2 * n - 2} frames, crf {crf}, {mb:.1f} MB, {time.time() - t0:.0f}s")

    ids = write_manifest()
    missing = [specs.ident(i) for i in range(len(specs.SPECS)) if specs.ident(i) not in ids]
    print(f"\ningested {len(done)}; site now has classic + {len(ids)} Kling eyes ({len(ids) + 1} total)")
    if unmatched:
        print(f"unmatched: {len(unmatched)}")
    if missing:
        print(f"still missing ({len(missing)}): {', '.join(missing)}")


if __name__ == "__main__":
    main()
