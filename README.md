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

## Type

The line "What do you feel?" is set in AUTHENTIC Sans 90 (`fonts/AUTHENTICSans-90.woff2`,
10 KB), by AUTHENTIC, distributed under the WTFPL — self-hosting is unrestricted.
Size is fluid: `clamp(13px, 1.5vw, 18px)`, pinned to the bottom above the iOS safe area.

## Framing

The video uses `object-fit: cover` on landscape viewports and switches to `contain`
below a 3:2 aspect ratio. On a tall phone `cover` crops a 16:9 clip so hard that the
eyes fall off the sides; the clip is on black, so `contain` letterboxes invisibly.
If your real clip is framed tighter or wider, that 3:2 threshold is the knob to turn.

## Custom domain

Add a `CNAME` file containing the bare hostname, then at your registrar point
that host at `jamminstein.github.io` with a CNAME record. Apex domains use
GitHub's A records instead. HTTPS provisions automatically once DNS resolves.
