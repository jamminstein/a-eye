#!/usr/bin/env bash
# Rebuild eye.mp4: grade to black and white, ping-pong the clip (forward then
# reverse, forever), and punch in with hard cuts.
#
#   tools/pingpong.sh ~/path/to/source.mp4
#
# The ping-pong is what makes the loop seamless -- no fade, no crossfade, no
# softening. Forward ends on frame N-1 and the reverse begins on N-2, so the
# turnaround and the loop wrap are both ordinary adjacent-frame steps. Grain is
# added in the browser, not here.
set -euo pipefail
SRC="${1:?usage: tools/pingpong.sh <source-clip>}"
cd "$(dirname "$0")/.."

Z="${ZOOM:-3.0}"                 # hard-cut magnification; 3x still holds up at 1080p
CX="${CUT_X:-1050}"; CY="${CUT_Y:-600}"   # pupil, while the eye looks at camera
# Cut windows, in seconds on the ping-ponged timeline. Two quick punches near the
# "looking at you" phase, mirrored in the reverse pass.
WINDOWS="${CUTS:-between(t,5.0,5.45)+between(t,5.85,6.30)+between(t,59.70,60.15)+between(t,60.55,61.0)}"

N=$(ffprobe -v error -select_streams v -count_frames -show_entries stream=nb_read_frames -of csv=p=0 "$SRC")
LAST=$((N-2))

echo "==> ping-pong ($N frames -> $((N+N-2)))"
# Drop the duplicated end frames from the reversed half, or the turnaround and
# the loop wrap each stutter on a repeated frame.
ffmpeg -y -hide_banner -loglevel error -i "$SRC" -filter_complex \
"[0:v]hue=s=0,split[a][b];[b]reverse,select='between(n,1,$LAST)',setpts=N/FRAME_RATE/TB[r];[a][r]concat=n=2:v=1:a=0[v]" \
-map "[v]" -an -c:v libx264 -preset veryfast -crf 12 -pix_fmt yuv420p /tmp/aeye-pp.mp4

ZF="(1+($Z-1)*($WINDOWS))"
echo "==> hard cuts at ${Z}x"
# crop's in_w/in_h are evaluated once at init, so clamp bounds are written out
# explicitly -- using in_w/in_h pins x,y to the top-left corner.
ffmpeg -y -hide_banner -loglevel error -i /tmp/aeye-pp.mp4 -vf \
"scale=w='ceil(1920*$ZF/2)*2':h='ceil(1080*$ZF/2)*2':eval=frame:flags=bicubic,\
crop=1920:1080:x='clip($CX*$ZF-960,0,1920*$ZF-1920)':y='clip($CY*$ZF-540,0,1080*$ZF-1080)'" \
-an -c:v libx264 -preset veryfast -crf 12 -pix_fmt yuv420p /tmp/aeye-cuts.mp4

echo "==> encode"
TARGET_MB="${TARGET_MB:-30}" ./encode.sh /tmp/aeye-cuts.mp4

echo "==> seam check"
ffmpeg -y -hide_banner -loglevel error -i eye.mp4 -vf "select='eq(n,0)+eq(n,400)+eq(n,401)'" -vsync 0 -frames:v 3 /tmp/sc_%d.png
ffmpeg -y -hide_banner -loglevel error -sseof -0.05 -i eye.mp4 -frames:v 1 -update 1 /tmp/sc_last.png
echo -n "  loop wrap:        "; ffmpeg -hide_banner -i /tmp/sc_last.png -i /tmp/sc_1.png -lavfi psnr -f null - 2>&1 | grep -io 'average:[0-9.]*' | tail -1
echo -n "  adjacent control: "; ffmpeg -hide_banner -i /tmp/sc_2.png -i /tmp/sc_3.png -lavfi psnr -f null - 2>&1 | grep -io 'average:[0-9.]*' | tail -1
