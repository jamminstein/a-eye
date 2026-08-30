#!/usr/bin/env bash
# Rebuild eye.mp4: grade to black and white, and manufacture a loop point by
# diving into the pupil and fading to black at the tail, mirrored at the head.
#
#   tools/plunge.sh ~/path/to/source.mp4
#
# The clip opens inside the black pupil, pulls out, plays, then plunges back in.
# Both end frames are pure black, so `<video loop>` has an exact seam. Grain is
# added in the browser, not here.
set -euo pipefail
SRC="${1:?usage: tools/plunge.sh <source-clip>}"
cd "$(dirname "$0")/.."

R="${PLUNGE:-1.3}"        # length of the dive at each end, seconds
ZMAX="${ZOOM:-5.0}"       # beyond ~5x a 1080p source turns to mush, and the
                          # scaled intermediate gets very large (1920*ZMAX wide)
FADE="${FADE:-0.45}"
CX0="${HEAD_X:-1056}"; CY0="${HEAD_Y:-596}"   # pupil in the opening frame
CX1="${TAIL_X:-290}";  CY1="${TAIL_Y:-180}"   # pupil in the closing frame

D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")
TE=$(python3 -c "print(f'{$D-$R:.6f}')")
# end the fade a frame early so the final frame is genuinely black, not 90% there
FO=$(python3 -c "print(f'{$D-$FADE-0.1:.6f}')")

US="clip(t/$R,0,1)"; UE="clip((t-$TE)/$R,0,1)"
SS="(1-($US*$US*(3-2*$US)))"; SE="(($UE*$UE*(3-2*$UE)))"
ZF="(1+($ZMAX-1)*($SS+$SE))"
# centre is irrelevant while ZF==1 (x,y clamp to 0), so blend toward frame centre
CX="($CX0*$SS+$CX1*$SE+960*(1-$SS-$SE))"
CY="($CY0*$SS+$CY1*$SE+540*(1-$SS-$SE))"

echo "==> plunge ${ZMAX}x over ${R}s at each end"
# crop's in_w/in_h are evaluated once at init, so clamp bounds are written out
# explicitly -- using in_w/in_h pins x,y to the top-left corner.
ffmpeg -y -hide_banner -loglevel error -i "$SRC" -vf \
"hue=s=0,scale=w='ceil(1920*$ZF/2)*2':h='ceil(1080*$ZF/2)*2':eval=frame:flags=bicubic,\
crop=1920:1080:x='clip($CX*$ZF-960,0,1920*$ZF-1920)':y='clip($CY*$ZF-540,0,1080*$ZF-1080)',\
fade=t=in:st=0:d=$FADE,fade=t=out:st=$FO:d=$FADE" \
-an -c:v libx264 -preset veryfast -crf 12 -pix_fmt yuv420p /tmp/aeye-plunge.mp4

echo "==> encode"
TARGET_MB="${TARGET_MB:-24}" ./encode.sh /tmp/aeye-plunge.mp4

echo "==> share image (poster.jpg is the black opening frame)"
ffmpeg -y -hide_banner -loglevel error -ss 6 -i eye.mp4 -frames:v 1 -q:v 4 share.jpg

echo "==> seam check"
ffmpeg -y -hide_banner -loglevel error -i eye.mp4 -vf "select=eq(n\,0),scale=160:90,format=gray" -frames:v 1 -f rawvideo /tmp/s0.raw
python3 -c "
d=open('/tmp/s0.raw','rb').read(); print(f'  first frame mean luma {sum(d)/len(d):.2f} (0.00 = exact loop)')"
