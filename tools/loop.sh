#!/usr/bin/env bash
# Rebuild eye.mp4 from the original clip: crossfade the loop seam, dive into one
# eye, grade to black and white, encode. Grain is added in the browser, not here.
#
#   tools/loop.sh ~/path/to/source.mp4
set -euo pipefail
SRC="${1:?usage: tools/loop.sh <source-clip>}"
cd "$(dirname "$0")/.."

X="${XFADE:-1.0}"            # crossfade length, seconds
T0="${DIVE_AT:-8.0}"         # when the dive starts
RI="${DIVE_IN:-0.7}"; H="${DIVE_HOLD:-1.0}"; RO="${DIVE_OUT:-0.7}"
ZOOM="${DIVE_ZOOM:-2.6}"     # beyond ~3x a 1080p source goes soft
CX="${DIVE_X:-1540}"; CY="${DIVE_Y:-650}"   # eye centre in source pixels

D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")
OFF=$(python3 -c "print(f'{$D - 2*$X:.6f}')")
T1=$(python3 -c "print($T0+$RI+$H)")

echo "==> crossfade ${X}s at ${OFF}s"
ffmpeg -y -hide_banner -loglevel error -i "$SRC" -filter_complex \
"[0:v]hue=s=0,split=2[a][b];\
[a]trim=0:${X},setpts=PTS-STARTPTS[head];\
[b]trim=${X}:${D},setpts=PTS-STARTPTS[body];\
[body][head]xfade=transition=fade:duration=${X}:offset=${OFF}[v]" \
-map "[v]" -an -c:v libx264 -preset veryfast -crf 12 -pix_fmt yuv420p /tmp/aeye-xfade.mp4

UIN="clip((t-$T0)/$RI,0,1)"; UOUT="clip((t-$T1)/$RO,0,1)"
Z="(($UIN*$UIN*(3-2*$UIN))*(1-($UOUT*$UOUT*(3-2*$UOUT))))"
ZF="(1+($ZOOM-1)*$Z)"

echo "==> dive to ${ZOOM}x at ${T0}s"
# crop's in_w/in_h are evaluated once at init, so the clamp bounds are written out
# explicitly -- using in_w/in_h pins x,y to the top-left corner.
ffmpeg -y -hide_banner -loglevel error -i /tmp/aeye-xfade.mp4 -vf \
"scale=w='ceil(1920*$ZF/2)*2':h='ceil(1080*$ZF/2)*2':eval=frame:flags=bicubic,\
crop=1920:1080:x='clip($CX*$ZF-960,0,1920*$ZF-1920)':y='clip($CY*$ZF-540,0,1080*$ZF-1080)'" \
-an -c:v libx264 -preset veryfast -crf 12 -pix_fmt yuv420p /tmp/aeye-dive.mp4

echo "==> encode"
TARGET_MB="${TARGET_MB:-24}" ./encode.sh /tmp/aeye-dive.mp4
