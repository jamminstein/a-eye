#!/usr/bin/env python3
"""Make the starting frames for the 55 eyes with an OpenAI image model.

    kling/make_frames.py --only 2,8,49 --model gpt-image-2 --out kling/pilot
    kling/make_frames.py                       # all 55 into kling/frames

Standard library only. The key comes from the macOS Keychain (service
openai-api-key), same as the openai-image MCP. Skips frames that already exist,
so it is safe to re-run after a failure.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import specs  # noqa: E402

# Approximate USD per 1024x1024 image (gpt-image-2 table in openai-image-mcp); scaled by pixels.
BASE_USD = {"low": 0.006, "medium": 0.053, "high": 0.211}


def api_key():
    k = os.environ.get("OPENAI_API_KEY")
    if k:
        return k
    return subprocess.run(
        ["/usr/bin/security", "find-generic-password", "-s", "openai-api-key", "-w"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()


def one(i, args, key, out_dir, lock, log_path):
    ident = specs.ident(i)
    path = out_dir / f"{ident}.jpg"
    if path.exists() and not args.force:
        return ident, "exists", 0.0
    prompt = specs.frame_prompt(specs.SPECS[i])
    body = {
        "model": args.model,
        "prompt": prompt,
        "size": args.size,
        "quality": args.quality,
        "n": 1,
        "output_format": "jpeg",
        "output_compression": 95,
    }
    data = json.dumps(body).encode()
    last = ""
    for attempt in range(5):
        req = urllib.request.Request(
            "https://api.openai.com/v1/images/generations", data=data,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            raw = base64.b64decode(d["data"][0]["b64_json"])
            path.write_bytes(raw)
            w, h = (int(x) for x in args.size.split("x"))
            usd = BASE_USD[args.quality] * (w * h) / (1024 * 1024)
            with lock, open(log_path, "a") as f:
                f.write(json.dumps({"id": ident, "model": args.model, "size": args.size,
                                    "quality": args.quality, "bytes": len(raw),
                                    "usd_est": round(usd, 3), "t": int(time.time())}) + "\n")
            return ident, "ok", usd
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:400]
            last = f"HTTP {e.code}: {msg}"
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(8 * (attempt + 1))
                continue
            break  # 400 (policy, bad param) will not improve on retry
        except Exception as e:  # network
            last = repr(e)
            time.sleep(5 * (attempt + 1))
    return ident, "FAILED " + last, 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma list of 1-based numbers, e.g. 2,8,49")
    ap.add_argument("--model", default="gpt-image-2")
    ap.add_argument("--size", default="2048x1152")
    ap.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    ap.add_argument("--out", default=str(HERE / "frames"))
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    idx = [int(x) - 1 for x in args.only.split(",")] if args.only else list(range(len(specs.SPECS)))
    key = api_key()
    lock = threading.Lock()
    log_path = out_dir / "log.jsonl"
    total = 0.0
    failed = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(one, i, args, key, out_dir, lock, log_path) for i in idx]
        for f in as_completed(futs):
            ident, status, usd = f.result()
            total += usd
            print(f"{ident}  {status}", flush=True)
            if status.startswith("FAILED"):
                failed.append(ident)
    print(f"done: {len(idx) - len(failed)}/{len(idx)} ok, ~${total:.2f} estimated, failed: {failed or 'none'}")


if __name__ == "__main__":
    main()
