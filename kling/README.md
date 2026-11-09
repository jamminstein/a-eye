# 60 eyes: from frames to the site

OpenAI shut its video API (Sora) down on 2026-09-24 and named no replacement, so the clips
are made in Kling. OpenAI's image model makes the starting frames; Kling animates them;
`ingest.py` turns Kling's downloads into site assets.

    specs.py         the 60 eyes: who, look, light, the Kling motion prompt for each
    make_frames.py   frames with gpt-image-2.6-sunburst  ->  frames/eye-01.jpg ... eye-60.jpg
    build_sheet.py   sheet.html (work page, open it) and PROMPTS.md (plain text)
    ingest.py        raw/*.mp4  ->  ../clips/eye-NN.mp4 + .jpg, and the clip list in ../index.html

## Doing the Kling part

1. Open `sheet.html` (double-click it). Batches of five.
2. For each card: **Download frame**, **Copy prompt**, in Kling: Image to Video, upload the
   frame as the first frame, paste the prompt, paste the negative prompt (button at the top).
3. Settings that matter: Professional (1080p), 10 s, 16:9, camera movement none, sound off,
   creativity toward relevance (about 0.6). Small natural motion is the point; anything that
   zooms, morphs or "acts" is a retake.
4. Download every result into `kling/raw/` (or any folder: `ingest.py ~/Downloads/a-eye`). Names do not matter: `ingest.py` finds each
   clip's frame by comparing its first frame with the 60 frames. If two eyes look alike and
   it says "ambiguous", put the number in the name (`eye-07.mp4`).
5. Run `python3 kling/ingest.py` (or ask Claude to). It is incremental: run it after
   each batch, it only does the new clips.

Two takes of one frame are both kept: the second becomes `eye-07b`, its own clip in the
shuffle (the page never shows the same face twice running). Do not want one? Put `_` in front
of its file name before ingesting, or delete `clips/eye-07b.mp4` and `.jpg` and run
`ingest.py --rebuild-manifest`. `clips/sources.json` remembers which file became which clip,
so running ingest again on the same folder does nothing twice. To re-encode: `--force`.
The sheet marks eyes that already have a clip ("on the site"), so "hide done" shows what is left.

## What ingest does to a clip

Grades to black and white (`hue=s=0`, grain is added in the browser), then ping-pongs it:
forward, then reverse, minus the duplicated end frames. A 15 s clip becomes a 30 s loop (10 s ones
20 s) with no seam and no crossfade, the same trick as `tools/pingpong.sh`. Drops the audio. Encodes
H.264 High, 1080p max, CRF 26 capped at 3 Mbit/s (re-encodes harder if a clip passes 7 MB),
faststart. The poster is the clip's first frame. A 30 s loop is 5 MB on average (the first 28:
161 MB), so about 350 MB for all 60 eyes. Nothing from the raw files (metadata, audio) is kept.

## The page

`index.html` carries the list (`/*clips*/[...]/*end*/`, rewritten by ingest) and picks an eye on
load from a shuffled bag in localStorage: all eyes are shown once before any repeats, and the
first of a fresh bag is never the one you just saw. `eye.mp4` is the original and stays in
the bag as `classic`.

    /?eye=eye-07    show that one (does not touch the bag)
    /#eye-07        same

If a clip fails to load, the page falls back to `classic`.

## Frames

Made 2026-11-05 with `gpt-image-2.6-sunburst`, 2048 x 1152, high quality, about $0.47 each
(about $24 for the set). Compared on the same two specs with `gpt-image-2` (too clean, stock
photo skin and sclera) and `gpt-image-2.6-flare` (raw, but skin picked up dark specks);
sunburst had the most documentary imperfection. The frames are colour on purpose: the
black-and-white grade happens at ingest, and colour gives Kling the most to work with.

Redo one: edit its spec in `specs.py`, then `python3 kling/make_frames.py --only 7 --force
--model gpt-image-2.6-sunburst`, then `python3 kling/build_sheet.py`. `frames/` is committed
(21 MB; regenerating costs about $24 and gives different people), so it is backed up with the repo.

What makes a frame read as a photograph, in the specs: a specific person, a specific light
and the actual room mirrored in the cornea with the photographer's silhouette, one honest
imperfection (scar, redness, white lashes, asymmetry), and nothing pretty on purpose.
