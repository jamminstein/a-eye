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

## Custom domain

Add a `CNAME` file containing the bare hostname, then at your registrar point
that host at `jamminstein.github.io` with a CNAME record. Apex domains use
GitHub's A records instead. HTTPS provisions automatically once DNS resolves.
