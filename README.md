# A-eye

A continuous AI stare. One page, black, two eyes looking at you. Nothing else.

Live: https://jamminstein.github.io/a-eye/

## Replacing the video

`eye.mp4` currently holds a procedurally-rendered placeholder. To swap in a real clip:

```bash
./encode.sh ~/path/to/your-clip.mp4
git add -A && git commit -m "new stare" && git push
```

GitHub Pages redeploys within about a minute.

`encode.sh` scales to 1080p max, encodes H.264 High / yuv420p with `+faststart`,
keeps the file under 20 MB (override with `TARGET_MB=40 ./encode.sh ...`), and
regenerates `poster.jpg` from the first frame.

**The clip should start and end on the same frame.** The page uses a plain
`<video loop>`, so a mismatched first/last frame shows a visible jump every
cycle. If your generator can't do that, the fix is two stacked `<video>`
elements crossfading the tail into the head.

## Regenerating the placeholder

```bash
node tools/make-placeholder.mjs eye.mp4
```

12 s, 25 fps, 1280×720. All motion (pupil hippus, two blinks) is periodic over
the clip length, so it loops seamlessly.

## The look

The clip is graded to black and white at encode time and the grain is added in the
browser, not baked in:

```bash
GRADE="hue=s=0" TARGET_MB=24 ./encode.sh <source>
```

Baking grain into the video was tried and abandoned. Synthetic noise is
near-incompressible: at CRF 21 with `-tune grain` the file passed 177 MB, and
forcing it down to 19 MB at 8300 kbps spent the whole budget on noise and returned
macroblocking and smeared skin instead of grain. Overlaying instead keeps the
image sharp *and* the grain sharp, and the clean master is smaller (13 MB).

The overlay is `grain.png` (256×256 tiling noise, 70 KB) on a fixed 200% layer at
16% opacity, `mix-blend-mode: overlay`, nudged between eight offsets with
`steps(1)` so it churns per frame instead of sliding. Reduced-motion viewers keep
the texture and lose the churn. To change intensity, edit `#grain { opacity }`.

## The loop, and the plunge

The source clip has no natural loop -- the eye drifts continuously and never
returns to its opening position. Looped raw the seam measured 12.6 dB PSNR
against a 37.4 dB adjacent-frame control, and a frame-by-frame search found no
better cut point anywhere in the clip (best candidate 15.6 dB).

So the loop point is manufactured rather than found. `tools/plunge.sh` dives 5x
into the pupil over the last 1.3 s, fading to black as it goes, and mirrors that
move at the head -- the clip opens inside the black pupil and pulls back out.
Both end frames are pure black (mean luma 0.00), so the loop point is exact and
the motion reads as one continuous plunge in and out.

Not a crossfade: nothing dissolves through anything. The darkness is where the
dive ends up.

`poster.jpg` is therefore a black frame, which is correct -- it matches frame 0,
so there is no flash before playback. `share.jpg` is a separate mid-clip frame
used for `og:image`.

## Framing

There is no text on the page. `fonts/AUTHENTICSans-90.woff2` is kept in the repo
for if type ever returns, but nothing references it.

The video uses `object-fit: cover` on landscape viewports and switches to `contain`
below a 3:2 aspect ratio. On a tall phone `cover` crops a 16:9 clip so hard that the
eyes fall off the sides; the clip is on black, so `contain` letterboxes invisibly.
If your real clip is framed tighter or wider, that 3:2 threshold is the knob to turn.

## Custom domain

Add a `CNAME` file containing the bare hostname, then at your registrar point
that host at `jamminstein.github.io` with a CNAME record. Apex domains use
GitHub's A records instead. HTTPS provisions automatically once DNS resolves.
