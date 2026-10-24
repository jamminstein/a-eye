#!/usr/bin/env bash
# Cut favicon.gif from eye.mp4: the wide shot drifting up to the lid closing,
# then the same frames in reverse so it opens again -- tools/pingpong.sh at
# favicon scale, so the loop has no seam and the blink reads both ways.
#
#   tools/favicon.sh
#   START=12 END=15.4 CROP=900:900:600:180 tools/favicon.sh
#
# Only Firefox animates favicons. Chrome and Safari show the first frame, so
# START must land on an open eye.
set -euo pipefail
cd "$(dirname "$0")/.."

START="${START:-12}"            # wide shot, eye open
END="${END:-15.4}"              # a couple of frames after the lid shuts
FPS="${FPS:-12}"
SIZE="${SIZE:-64}"
COLORS="${COLORS:-64}"
CROP="${CROP:-900:900:600:180}" # w:h:x:y -- a square around the iris at 1080p
DUR=$(awk -v a="$START" -v b="$END" 'BEGIN{print b-a}')

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
mkdir "$TMP/seg" "$TMP/seq"

ffmpeg -y -hide_banner -loglevel error -ss "$START" -t "$DUR" -i eye.mp4 \
  -vf "fps=$FPS,crop=$CROP,scale=$SIZE:$SIZE:flags=lanczos" "$TMP/seg/%03d.png"

# Forward 1..N, then N-1..2. The end frames are not repeated, so the
# turnaround and the loop wrap are ordinary adjacent-frame steps.
N=$(ls "$TMP/seg" | wc -l | tr -d ' ')
i=1
for k in $(seq 1 "$N") $(seq $((N-1)) -1 2); do
  ln -s "$TMP/seg/$(printf %03d.png "$k")" "$TMP/seq/$(printf %03d.png "$i")"
  i=$((i+1))
done

ffmpeg -y -hide_banner -loglevel error -framerate "$FPS" -i "$TMP/seq/%03d.png" -filter_complex \
  "[0:v]split[a][b];[a]palettegen=max_colors=$COLORS:stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle" \
  -loop 0 favicon.gif

echo "favicon.gif  $((i-1)) frames  ${SIZE}x${SIZE}  $(du -h favicon.gif | cut -f1)"
