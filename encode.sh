#!/usr/bin/env bash
# Turn a generated clip into the web assets the site serves.
#
#   ./encode.sh ~/Downloads/my-eyes.mp4
#
# Produces eye.mp4 (H.264 High / yuv420p / faststart -- plays everywhere) and
# poster.jpg (first frame, shown before the video decodes). Keeps the video
# under TARGET_MB by falling back to a two-pass bitrate encode if CRF overshoots.
set -euo pipefail

SRC="${1:-}"
[ -n "$SRC" ] || { echo "usage: ./encode.sh <source-clip>" >&2; exit 1; }
[ -f "$SRC" ] || { echo "no such file: $SRC" >&2; exit 1; }

cd "$(dirname "$0")"
TARGET_MB="${TARGET_MB:-20}"
MAX_BYTES=$(( TARGET_MB * 1000 * 1000 ))
OUT=eye.mp4
POSTER=poster.jpg

# Cap at 1080p; anything larger costs bitrate the effect doesn't need.
SCALE="scale='min(1920,iw)':'min(1080,ih)':force_original_aspect_ratio=decrease:flags=lanczos,scale=trunc(iw/2)*2:trunc(ih/2)*2"

echo "==> pass: crf"
ffmpeg -y -hide_banner -loglevel error -i "$SRC" \
  -an -vf "$SCALE" \
  -c:v libx264 -preset slow -crf 21 -profile:v high -pix_fmt yuv420p \
  -movflags +faststart "$OUT"

SIZE=$(wc -c < "$OUT" | tr -d ' ')
if [ "$SIZE" -gt "$MAX_BYTES" ]; then
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")
  # 96% of budget in video bitrate, leaving room for container overhead.
  BR=$(awk -v b="$MAX_BYTES" -v d="$DUR" 'BEGIN{printf "%d", (b*8*0.96)/d/1000}')
  echo "==> ${SIZE} bytes over budget; two-pass at ${BR}k"
  ffmpeg -y -hide_banner -loglevel error -i "$SRC" -an -vf "$SCALE" \
    -c:v libx264 -preset slow -b:v "${BR}k" -profile:v high -pix_fmt yuv420p \
    -pass 1 -f null /dev/null
  ffmpeg -y -hide_banner -loglevel error -i "$SRC" -an -vf "$SCALE" \
    -c:v libx264 -preset slow -b:v "${BR}k" -profile:v high -pix_fmt yuv420p \
    -pass 2 -movflags +faststart "$OUT"
  rm -f ffmpeg2pass-*.log ffmpeg2pass-*.log.mbtree
fi

echo "==> poster"
ffmpeg -y -hide_banner -loglevel error -i "$OUT" -frames:v 1 -q:v 3 "$POSTER"

echo
echo "eye.mp4    $(du -h "$OUT" | cut -f1)"
echo "poster.jpg $(du -h "$POSTER" | cut -f1)"
echo
echo "next:  git add -A && git commit -m 'new stare' && git push"
