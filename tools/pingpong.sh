#!/usr/bin/env bash
# Rebuild eye.mp4: grade to black and white and ping-pong the clip -- forward,
# then reverse, forever.
#
#   tools/pingpong.sh ~/path/to/source.mp4
#
# The ping-pong is what makes the loop seamless: forward ends on frame N-1 and
# the reverse begins on N-2, so both the turnaround and the loop wrap are
# ordinary adjacent-frame steps. No fade, no crossfade, no zoom, no softening.
# Grain is added in the browser, not here.
set -euo pipefail
SRC="${1:?usage: tools/pingpong.sh <source-clip>}"
cd "$(dirname "$0")/.."

N=$(ffprobe -v error -select_streams v -count_frames -show_entries stream=nb_read_frames -of csv=p=0 "$SRC")
LAST=$((N-2))

echo "==> ping-pong ($N frames -> $((N+N-2)))"
# Dropping the duplicated end frames is essential: without it the turnaround and
# the loop wrap each stutter on a repeated frame.
ffmpeg -y -hide_banner -loglevel error -i "$SRC" -filter_complex \
"[0:v]hue=s=0,split[a][b];[b]reverse,select='between(n,1,$LAST)',setpts=N/FRAME_RATE/TB[r];[a][r]concat=n=2:v=1:a=0[v]" \
-map "[v]" -an -c:v libx264 -preset veryfast -crf 12 -pix_fmt yuv420p /tmp/aeye-pp.mp4

echo "==> encode"
TARGET_MB="${TARGET_MB:-30}" ./encode.sh /tmp/aeye-pp.mp4

echo "==> seam check"
ffmpeg -y -hide_banner -loglevel error -i eye.mp4 -vf "select='eq(n,0)+eq(n,400)+eq(n,401)'" -vsync 0 -frames:v 3 /tmp/sc_%d.png
ffmpeg -y -hide_banner -loglevel error -sseof -0.05 -i eye.mp4 -frames:v 1 -update 1 /tmp/sc_last.png
echo -n "  loop wrap:        "; ffmpeg -hide_banner -i /tmp/sc_last.png -i /tmp/sc_1.png -lavfi psnr -f null - 2>&1 | grep -io 'average:[0-9.]*' | tail -1
echo -n "  adjacent control: "; ffmpeg -hide_banner -i /tmp/sc_2.png -i /tmp/sc_3.png -lavfi psnr -f null - 2>&1 | grep -io 'average:[0-9.]*' | tail -1
