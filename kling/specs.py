"""The 50 eyes.

Each spec has everything needed for two jobs:

  * the starting FRAME (made with an OpenAI image model): who, look, light, state
  * the Kling MOTION prompt (image-to-video): motion

kind:  macro = one eye fills the frame
       eye   = one eye with brow, temple and nose bridge
       pair  = both eyes, brows to cheekbones
side:  which eye (macro / eye only)

Rules every spec follows, because they are what separates a photograph from an
"AI eye": a specific person, a specific light and a specific thing mirrored in
the cornea, one honest imperfection (scar, redness, asymmetry, a stray hair),
and a motion that is small and physical. Nothing glows, nothing is symmetrical,
nothing is pretty on purpose.
"""

# ---------------------------------------------------------------- shared text

RECIPE = (
    "Unposed documentary photograph, unretouched RAW file straight from the camera: "
    "Canon EOS R5, RF 100mm f/2.8L Macro, f/4, ISO 640, natural or practical light only, "
    "no flash, no studio lighting, no softbox, no ring light. "
    "Real skin: visible pores, fine vellus hair, tiny uneven marks and fine creases, "
    "uneven tone, no smoothing, no airbrushing, no glow, no beauty retouching. "
    "Real eye: irregular iris fibres and crypts that are not perfectly radial, a darker uneven "
    "limbal ring, a slightly off-round pupil, a few faint capillaries in the sclera, a wet tear "
    "meniscus along the lower lid, and the cornea mirroring the actual room as a small distorted "
    "image of the real light source together with the dark silhouette of the photographer. "
    "Lashes of uneven length and thickness, some crossing, some clumped, a few strays; brow hairs "
    "growing in different directions. "
    "Focus plane on the iris, with natural macro depth-of-field falloff on the lashes, lids and skin; "
    "faint sensor noise; slight softness toward the frame edges; accurate lens perspective. "
    "Asymmetric, imperfect and specific, like a single frame pulled from real documentary footage. "
    "Not a stock photo, not a portrait session, not CGI, not an illustration, not a render. "
    "No text, no logos, no watermark. 16:9 landscape."
)

FRAMING = {
    "macro": (
        "Extreme close-up macro of the {side} eye of {who}. The eye fills the whole frame and sits "
        "slightly off-centre; the brow cuts across the top edge and the upper cheek across the bottom "
        "edge; no other facial feature is visible."
    ),
    "eye": (
        "Close-up of the {side} eye of {who}, with the eyebrow, the temple and the side of the nose "
        "bridge in frame; the eye sits in the middle third of the 16:9 frame, a little above centre."
    ),
    "pair": (
        "Tight horizontal crop of both eyes and the bridge of the nose of {who}, from the brows down "
        "to the upper cheekbones, nothing below the tip of the nose. The two eyes are slightly "
        "asymmetric, as real eyes are."
    ),
}

# Added to every Kling prompt: the camera does nothing, the eye does everything.
KLING_CAMERA = "Locked-off tripod macro shot, no zoom, no pan, no camera movement, natural skin micro-movement."

KLING_NEGATIVE = (
    "morphing, warping eyes, melting, flicker, jitter, extra pupils, changing iris colour, deformed "
    "pupil, extra or merged eyelashes, plastic or waxy skin, airbrushed, cartoon, CGI, 3D render, "
    "illustration, oversaturated, sharpening halos, zoom, camera shake, pan, tilt, text, watermark, "
    "subtitles, speaking, lip movement, head turning away, hands"
)

# ---------------------------------------------------------------------- eyes
# 20 macro, 14 eye, 16 pair.

SPECS = [
    # ------------------------------------------------------------------ macro
    dict(
        name="Dawn, chestnut", kind="macro", side="left",
        who="a woman in her early thirties of southern Italian descent",
        look="Chestnut-brown iris with a thin amber ring hugging the pupil and fine radial crypts; "
             "one pale hairline scar cutting through the outer end of the eyebrow; the first crow's "
             "feet at the outer corner; no makeup, a little dry skin on the lid.",
        light="Cold blue pre-dawn light from a tall window at camera-left; the cornea mirrors that "
              "window with its two thin mullions.",
        state="Looking straight into the lens, face relaxed, lids at rest, not smiling.",
        motion="Steady gaze into the lens. The pupil slowly opens as the room darkens a little. One "
               "unhurried blink around the fourth second, lashes settling after it. The eye then "
               "drifts a few degrees toward the window and comes back to the lens.",
    ),
    dict(
        name="Obsidian", kind="macro", side="right",
        who="a man in his early forties of Nigerian descent",
        look="Very dark brown iris, almost black, the pupil only just distinguishable inside it, a "
             "strong dark limbal ring; long thick lashes curving upward with a few that curl back "
             "onto the lid; deep brown skin with a faint natural sheen on the lid and a few tiny "
             "dry flakes; a sclera that is faintly warm-tinted with a few brown pigment specks near "
             "the edge, white-ish overall, not yellow.",
        light="A bright overcast window on one side: the cornea carries one large soft rectangle of "
              "light; a weak warm lamp fills the shadow side of the face.",
        state="Looking into the lens with quiet attention, lids relaxed.",
        motion="Almost still. The huge dark pupil breathes slightly with the light. A slow, heavy "
               "blink, then a long steady hold. The lashes catch the window light for a moment as "
               "the lid lifts.",
    ),
    dict(
        name="Glacier", kind="macro", side="left",
        who="a Norwegian man in his mid sixties",
        look="Pale grey-blue iris with a white starburst pattern near the pupil and a faint grey ring "
             "of arcus senilis at the iris edge; pale lashes that are nearly transparent at the base "
             "with slightly darker tips; thin freckled lid skin with a few blue veins showing; "
             "sun-damaged brow skin.",
        light="Hard white glare off snow, outdoors in winter; he is squinting very slightly; the cornea "
              "mirrors a pure white sky with the dark silhouette of the photographer and the dark "
              "line of a roof.",
        state="Looking into the lens, a slight squint against the glare.",
        motion="He squints a little harder as the glare brightens, the pupil pinning down to a small "
               "point. Then he relaxes, the lid softens and the pupil opens. A single slow blink. "
               "A tiny involuntary tremor in the lid.",
    ),
    dict(
        name="Screen light", kind="macro", side="right",
        who="a South Korean woman in her late twenties",
        look="Monolid with a smooth lid and no crease; short straight lashes pointing down; deep brown "
             "iris warming to amber near the pupil; a tiny beauty mark under the lower lashes; "
             "slightly dry, tired eye with a faint pink waterline.",
        light="Late night in a dark room lit only by a laptop: a cool blue-white glow from the lower "
              "left; the cornea mirrors the bright laptop screen as a small rectangle with faint "
              "horizontal bars of window layout, no readable text.",
        state="Eyes on the screen just below the lens, then lifting to the lens.",
        motion="Small fast saccades left to right as if reading, then a pause. The eye lifts up and "
               "settles on the lens. The screen's reflection brightens and dims as the picture "
               "changes. One quick blink.",
    ),
    dict(
        name="Wedge of brown", kind="macro", side="left",
        who="a mixed-heritage man in his mid twenties, West African and Scottish",
        look="Sectoral heterochromia: a blue-grey iris with a clear wedge of hazel brown at about four "
             "o'clock, the boundary irregular and feathered; thick dark lashes; light brown skin with "
             "a few freckles on the lid; a faint red line where the lower lid meets the eye.",
        light="Mid-afternoon sun bouncing off a pale wall into a plain room; the cornea mirrors a "
              "single bare ceiling lamp and a doorway.",
        state="Looking into the lens, a trace of curiosity, one brow a touch higher than the other.",
        motion="The gaze holds, then slides slowly to the left edge as if hearing something in the "
               "next room, pauses, and returns to the lens. The brow lowers. The pupil flexes once.",
    ),
    dict(
        name="Olive", kind="macro", side="right",
        who="an Irish woman in her early fifties",
        look="Olive-green iris with gold flecks around the pupil; lids slightly crepey; a few "
             "burst capillaries on the sclera and a pink, tired lower rim; fine lines fanning from "
             "the corner; faint freckles; grey coming into the brow hairs.",
        light="Late evening, a single tungsten bedside lamp to camera-right; the cornea mirrors the "
              "lamp bulb under its shade as a warm blob with a curved outline.",
        state="Looking into the lens, tired but present, lids a little heavy.",
        motion="Heavy lids lift and fall slowly. A long blink with a small struggle to reopen. The "
               "pupil is wide in the dim light and narrows slightly when she focuses back on the lens.",
    ),
    dict(
        name="Honey", kind="macro", side="left",
        who="a man in his early thirties of Punjabi descent",
        look="Honey-amber iris, translucent where the light passes through it so the texture of the "
             "fibres is visible like a cut gemstone; the pupil very small; dark curved lashes lit "
             "gold at the tips; warm brown skin with fine sun lines at the corner.",
        light="Low golden-hour sun striking from the side; the cornea carries one tiny hard hotspot "
              "of the sun plus the dark silhouette of the photographer; the iris glows from within.",
        state="Looking into the lens with a slight squint into the sun.",
        motion="The sun flares and fades as a cloud passes: the iris brightens, then deepens, the "
               "pupil opening in answer. A slow blink. The squint relaxes a little.",
    ),
    dict(
        name="Milk", kind="macro", side="right",
        who="an Ethiopian woman of about eighty-six",
        look="Dark brown iris with a thin milky haze across it from early cataract and a "
             "clear pale ring of arcus senilis at its edge; thin wrinkled lid skin folding in many "
             "tiny creases; sparse grey-white lashes; a wet, slightly reddened lower lid; "
             "deep-set eye.",
        light="Soft daylight from a curtained window; the cornea mirrors the pale window and a "
              "bit of white curtain.",
        state="Looking calmly and a little amused into the lens.",
        motion="A long, slow, very calm hold. The thin lid trembles faintly. One slow blink that "
               "takes its time. The pupil drifts a little as her attention moves, then returns "
               "to the lens.",
    ),
    dict(
        name="Pterygium", kind="macro", side="left",
        who="a man in his late fifties of Mexican and Indigenous descent, an outdoor worker",
        look="Dark brown iris; a small pinkish pterygium growing in from the nasal corner of the "
             "sclera; sun-cracked weathered skin with deep squint lines; thick short lashes "
             "bleached at the tips; salt-and-pepper brow.",
        light="Harsh midday sun from overhead: a hard brow shadow cuts across the upper half of the "
              "eye; the cornea mirrors a white sky, a hat brim and the photographer.",
        state="Looking into the lens, a squint against the light, unimpressed.",
        motion="He squints, the brow shadow shifting a little as the head settles. A slow "
               "dismissive blink. The eye widens a fraction, then narrows again, steady and "
               "unreadable.",
    ),
    dict(
        name="Night shift", kind="macro", side="right",
        who="a Black British woman in her mid forties",
        look="Dark brown iris, slightly bloodshot with a pink-red waterline; under-eye skin "
             "darker and a little puffy; a faint line of mascara residue at the base of the "
             "lashes; the beginnings of crow's feet; real tiredness, not styled.",
        light="Overhead fluorescent tubes in a hospital corridor at 4 a.m.; the cornea mirrors two "
              "long thin parallel white strips and a dim green exit sign in the distance.",
        state="Looking into the lens with flat, tired composure.",
        motion="Heavy lids. A slow blink that stays closed a half-second too long. The eye "
               "reopens and sharpens, the pupil narrowing under the tube lights. A tiny twitch "
               "in the lower lid.",
    ),
    dict(
        name="Held back", kind="macro", side="left",
        who="a Japanese man in his mid thirties",
        look="Dark brown iris; lids slightly flushed pink; the lower tear meniscus thickening and "
             "glassy, a few lashes stuck together by wetness; the lower lid red at the edge; no "
             "makeup, sweat-free skin; a tiny muscle tension at the outer corner.",
        light="Dusk through a window, soft and blue-grey; the cornea mirrors the window and a "
              "smear of the dim room.",
        state="Looking into the lens, holding it together, eyes brimming.",
        motion="The tear line swells slowly. He holds the gaze without blinking for as long as he "
               "can, then blinks once; a single droplet gathers on the lower lashes and hangs "
               "there without falling. The eye reopens, shining.",
    ),
    dict(
        name="Neon", kind="macro", side="right",
        who="a Filipina woman in her mid twenties",
        look="Dark brown iris; mascara slightly smudged at the outer corner; a small speck of "
             "glitter on the lid; an eyelash curled back at an odd angle; warm brown skin with "
             "a little shine from the heat of the night.",
        light="Outside a bar at night: a pink and cyan neon sign to the left lights the skin edge "
              "and mirrors in the cornea as two curved tubes of light.",
        state="Looking toward the lens, slightly amused, one corner of the eye lifting.",
        motion="The neon flickers once. Her eyes flick to the side, following someone walking "
               "past behind the camera, and come back to the lens with a half-smile. A quick, "
               "easy blink.",
    ),
    dict(
        name="Dashboard", kind="macro", side="left",
        who="a Lebanese man in his mid forties",
        look="Dark olive-brown iris with a thin lighter ring; thick low brow casting shade; dark "
             "circles; a few grey hairs in the brow; the lid skin slightly oily; unshaven skin "
             "just visible at the bottom edge.",
        light="Night driving: the dashboard glows a dim green-amber from below; amber sodium "
              "streetlights sweep across the face one after another; the cornea mirrors the "
              "windscreen and the road as a dark smear with moving points of light.",
        state="Looking into the lens, eyes calm and tired.",
        motion="Streetlight washes slide across the eye at a steady rhythm. His gaze flicks to the "
               "road ahead and returns to the lens. The pupil adjusts after each sweep of light. "
               "One slow blink.",
    ),
    dict(
        name="Candle", kind="macro", side="right",
        who="a woman of about seventy from Kerala, India",
        look="Hazel-brown iris with a cloudy white arcus ring and a slightly yellowed sclera; "
             "deep fine wrinkles around the eye; grey brow with long wiry hairs; wet lower lid; "
             "warm brown skin with a small age spot beside the eye.",
        light="Candlelight only, in an otherwise dark room: a small warm flame mirrors in the "
              "cornea as a tiny teardrop shape; deep soft shadows.",
        state="Looking steadily into the lens, serene.",
        motion="The candle flame flickers and the reflection in the cornea leans and recovers. "
               "The pupil is wide and narrows a touch when the flame flares. A long slow blink. "
               "The gaze never leaves the lens.",
    ),
    dict(
        name="Rain", kind="macro", side="left",
        who="a non-binary person in their early twenties, Black and Puerto Rican",
        look="Grey-green iris with a darker green rim; tiny raindrops on the lashes and on the "
             "cheekbone below; wet skin; a small silver stud near the end of the brow; a few "
             "freckles; a faint red edge to the lower lid from the cold.",
        light="Overcast evening in the rain, standing close to a window: street lights beyond "
              "the wet glass turn into soft round bokeh; the cornea mirrors the rain-streaked "
              "window and its bokeh.",
        state="Looking into the lens, composed, a little guarded.",
        motion="A raindrop on the lashes grows heavy, slides down and is flicked away by a "
               "blink. The eye stays on the lens. The bokeh lights behind the glass drift and "
               "pulse. A faint tightening around the eye.",
    ),
    dict(
        name="Pale blue", kind="macro", side="right",
        who="a Polish woman of nineteen",
        look="Very pale blue iris with a dark limbal ring, almost translucent; blonde lashes "
             "nearly invisible at the base and darker only at the tips; fair skin with fine "
             "freckles across the lid and a faint blue vein at the temple; tiny pink eyelid edge.",
        light="Flat, bright overcast daylight from a big window; the cornea mirrors a soft pale "
              "rectangle and a branch of a tree outside, blurred.",
        state="Looking into the lens, open and curious, brows slightly lifted.",
        motion="Curious: the head makes a tiny tilt and the pupil tracks it, the iris scanning as "
               "if reading the lens. The branch in the reflection sways. A quick blink, then a "
               "wide, clear hold.",
    ),
    dict(
        name="Hooded", kind="macro", side="left",
        who="a white American man of about fifty-two",
        look="Hazel-green iris, heavily hooded upper lid with a deep fold; thick grey eyebrow with "
             "long wild hairs; deep crow's feet; puffy lower lid; a visible small yellow "
             "pinguecula on the sclera.",
        light="Living room at night lit by a television: a flickering blue-white light on one "
              "side; the cornea mirrors a bright rectangle of a moving picture.",
        state="Looking into the lens, slightly skeptical.",
        motion="The television light changes, brightening and dimming the iris. A faint skeptical "
               "narrowing of the lid, brow settling. The gaze holds. A single slow blink. The "
               "hooded lid barely moves.",
    ),
    dict(
        name="White streak", kind="macro", side="right",
        who="a woman of about thirty-three of Dominican descent",
        look="Deep brown iris; poliosis: a small cluster of pure white lashes at the outer "
             "corner of the upper lid among the dark ones, with a matching white tuft in the "
             "brow above; a small mole on the lid; warm brown skin; no makeup.",
        light="Soft north window light on a grey morning; the cornea mirrors a pale window and a "
              "grey sky.",
        state="Looking into the lens, relaxed, with a hint of a smile around the eye.",
        motion="The pupil breathes. A slow blink; the white lashes catch the light as they close "
               "and open. A faint smile gathers at the corner of the eye and fades.",
    ),
    dict(
        name="Contact lens", kind="macro", side="left",
        who="a Brazilian woman in her late twenties",
        look="Light brown iris with the faint circular edge of a soft contact lens visible on the "
             "cornea, a tiny bubble trapped at one side; slightly pink waterline; long natural "
             "lashes, one slightly bent; a tiny scar on the lid; warm olive skin.",
        light="Bathroom mirror lit by a row of vanity bulbs: the cornea mirrors a curved arc of "
              "little round bulbs and the photographer; warm, a bit harsh.",
        state="Looking at the lens, concentrated, as if checking something.",
        motion="A hard blink to settle the lens, then a slower one. The tiny bubble shifts. The "
               "gaze holds, a little amused. The bulbs' reflection wobbles with the tiny "
               "movement of the head.",
    ),
    dict(
        name="After the swim", kind="macro", side="right",
        who="a Samoan man in his early thirties",
        look="Deep brown iris, very dark; thick brow with water beading on the hairs; a water "
             "droplet resting on the upper lashes; the sclera slightly pink from the chlorine; "
             "brown skin with a small old scar on the temple.",
        light="Bright afternoon sun directly behind and above the photographer: a hard glare; the "
              "cornea mirrors a tiny blown-out sun and a pale sky; skin has real sweat shine.",
        state="Looking into the lens, squinting at the sun, a flicker of a grin.",
        motion="He squints against the sun; the droplet on the lashes shivers and drops with a "
               "blink. The grin comes and goes in the muscles around the eye. The pupil is "
               "pinned small by the light.",
    ),

    # -------------------------------------------------------------------- eye
    dict(
        name="Round glasses", kind="eye", side="left",
        who="an African American man of about thirty-eight, wearing thin gold round glasses",
        look="Dark brown iris seen through the glasses, the lens slightly magnifying and bending "
             "the lid edge at the rim; a faint smudge and a hair on the lens; thin eyebrow with "
             "a small notch cut into it; short lashes; the nose pad leaving a tiny pressure mark.",
        light="Afternoon window light from the left throws a clear reflection onto the glasses "
              "lens, a soft pale rectangle that partly hides the eye; the cornea also mirrors "
              "the window.",
        state="Looking over a faint reflection straight into the lens, relaxed.",
        motion="The reflection on the lens drifts as a cloud passes. The eye holds the lens. A "
               "tiny brow lift, then a slow blink behind the glass. The brow settles.",
    ),
    dict(
        name="Half a smile", kind="eye", side="right",
        who="a Japanese woman of about sixty-three",
        look="Dark brown iris, eye narrowed into a smile with crow's feet fanned out to the "
             "temple; thin grey brow with a few dark hairs; age spots on the temple; crepey "
             "lid; a few white lashes; no makeup.",
        light="Warm early-evening kitchen light from a hanging pendant lamp above and in front; "
              "the cornea mirrors the pendant as a small warm bell shape.",
        state="Looking into the lens, eyes crinkled, a smile just beginning.",
        motion="The smile deepens slowly, the crow's feet gathering, the lower lid lifting, the "
               "eye almost closing. Then it eases back to a calm look. A soft, slow blink "
               "in the middle.",
    ),
    dict(
        name="Freckled", kind="eye", side="left",
        who="a Scottish man of twenty-nine with ginger hair",
        look="Grey-green iris with a brown fleck near the pupil; ginger lashes and brow, pale at "
             "the roots; freckles across the lid, temple and nose bridge; peeling sunburn on the "
             "nose; pink lower lid.",
        light="Soft grey daylight from an overcast sky outdoors, slight breeze; the cornea mirrors "
              "a bright grey dome of sky and a dark line of a hedge.",
        state="Looking into the lens, squinting a little against the bright sky.",
        motion="A breeze moves a few strands of red hair across the brow. He blinks once to clear "
               "them. The gaze stays on the lens. The sky's reflection brightens slightly as "
               "the cloud thins.",
    ),
    dict(
        name="The scar", kind="eye", side="right",
        who="an Afro-Caribbean man in his late forties",
        look="Dark brown iris with a slight yellow tinge in the sclera; a thin old scar running "
             "through the eyebrow and down onto the lid; a few grey hairs in the brow; fine "
             "grey stubble at the very top of the cheek; the lower lid slightly drooping.",
        light="A single practical lamp from the side at camera-left; hard shadow falls from the "
              "brow across the eye; the cornea mirrors the lamp as a small bright shape.",
        state="Looking into the lens, steady, giving nothing away.",
        motion="Steady stare. A muscle tightens briefly along the jaw so the cheek lifts a "
               "fraction and the lower lid rises. One slow, deliberate blink. The shadow "
               "from the brow barely moves.",
    ),
    dict(
        name="Patches", kind="eye", side="left",
        who="a South Asian woman of about thirty-four with vitiligo",
        look="Hazel-brown iris; pale depigmented patches of skin on the lid and around the "
             "eye, edges irregular; a few brown freckles on the patches; dark brow; natural "
             "lashes; a soft crease above the lid.",
        light="Bright soft daylight from a window to the right; the cornea mirrors a window "
              "frame and the room beyond; a gentle fall-off of light on the cheek.",
        state="Looking into the lens, calm and unhurried.",
        motion="A calm gaze. The light moves softly as a cloud shifts. A slow blink. Tiny "
               "movements of the iris as she focuses. The faintest smile at the outer corner.",
    ),
    dict(
        name="Waking", kind="eye", side="right",
        who="a person in their early twenties, East Asian and white, androgynous",
        look="Dark brown iris, sleep-heavy lids with a puffy upper lid; messy hair falling across "
             "the brow; a pillow crease pressed into the cheek; a bit of sleep crust in the lashes; "
             "slightly dry lips not in frame.",
        light="Soft morning light through a bedroom window at the side, with a bed-sheet fold in "
              "shadow; the cornea mirrors the window and a bit of white bedding.",
        state="Looking sleepily toward the lens, lids half-lowered.",
        motion="Heavy lids sink, then fight back up. A slow blink; the eye opens a little wider "
               "and sharpens on the lens. The pupil narrows in the brightening light. A loose "
               "strand of hair moves with a breath.",
    ),
    dict(
        name="Wind", kind="eye", side="left",
        who="an Indigenous Andean woman of about fifty-five",
        look="Dark brown iris; wind-chapped skin with red high-altitude cheeks and fine lines; "
             "the edge of a wool hat across the top of the frame; thick black brows with grey; "
             "short straight lashes; a deep brown, very clear gaze.",
        light="Bright thin high-altitude daylight, hard sun at the side; the cornea mirrors a "
              "pale sky and a ridge of mountain as a tiny dark line.",
        state="Looking into the lens, level and unembarrassed.",
        motion="Wind moves a strand of hair across the brow; she blinks against it and the "
               "strand drifts away. The gaze comes back and holds. A slight squint when the "
               "sun brightens.",
    ),
    dict(
        name="Last night's liner", kind="eye", side="right",
        who="a Black woman of about thirty, a night out ending",
        look="Dark brown iris; a bold black gel liner wing that has smudged a little under the "
             "eye and into the crease; gold shimmer on the lid worn thin; mascara clumps on "
             "the lashes; dewy skin from the heat; one tiny gold fleck on the cheekbone.",
        light="Warm bar light with string lights in the background as bokeh; the cornea mirrors "
              "a few little round bulbs and the dark shape of the photographer.",
        state="Looking toward the lens, loose and relaxed.",
        motion="She tracks something moving behind the camera, then returns. A slow blink. "
               "The little bulbs in the reflection twinkle. Her eye softens.",
    ),
    dict(
        name="Heavy lid", kind="eye", side="left",
        who="an Italian man of about seventy-four",
        look="Grey-brown iris with a pale arcus; mild ptosis so the upper lid hangs a little "
             "over the iris; thick white-grey eyebrow with long wild hairs; liver spots on the "
             "temple; deep folds; red and wet lower lid.",
        light="Soft window light from the right, a warm lamp behind; the cornea mirrors a tall "
              "pale window; skin has a papery look.",
        state="Looking into the lens, patient, brow slightly raised to lift the lid.",
        motion="He raises the brow to lift the heavy lid a little, the forehead creasing; the "
               "eye widens and holds; then it relaxes again. A very slow blink. The old eye "
               "is calm.",
    ),
    dict(
        name="Platform", kind="eye", side="right",
        who="a Chinese man of about forty-nine",
        look="Dark brown iris with a hint of grey; a slight monolid fold; dark circles; a few "
             "coarse grey hairs in the brow; the skin sallow under artificial light; an "
             "evenly narrowed look.",
        light="A subway platform: cool fluorescent tube light overhead and the green-white of "
              "a train arriving; the cornea mirrors two parallel tubes and a moving bright "
              "window of a train.",
        state="Looking into the lens, narrowed and skeptical.",
        motion="A train passes: bright rectangles slide across the cornea and the lids narrow "
               "against the flicker. The skeptical look sharpens. One slow blink as the train "
               "stops.",
    ),
    dict(
        name="Golden hour hazel", kind="eye", side="left",
        who="a Mexican American woman in her late thirties",
        look="Hazel iris with a green rim and brown centre, visibly textured; thick natural lashes "
             "with a little mascara; a faint dark line along the lid; light freckles; warm "
             "olive skin; a single laugh line.",
        light="Low gold sun through a window onto the face; the cornea mirrors the window and a "
              "tree outside; the iris lights up and reveals its fibres.",
        state="Looking into the lens, smiling softly with the eyes.",
        motion="The gaze drifts to the sun and returns, the pupil closing as it faces the light. "
               "A slow blink. The soft smile deepens slightly around the eye.",
    ),
    dict(
        name="Campfire", kind="eye", side="right",
        who="a Turkish man in his early thirties",
        look="Dark hazel iris; heavy brow, thick lashes; a few days of stubble at the very edge "
             "of the frame; a grain of ash on the cheek; skin flushed from heat.",
        light="Campfire at night: orange firelight on the left side of the face, deep black "
              "shadow on the right; the cornea mirrors tiny orange flames.",
        state="Looking into the lens with intensity, not smiling.",
        motion="The fire flickers and the flames in the reflection leap and sink. His gaze stays "
               "fixed; the eye narrows slightly, intense. A slow blink. A spark drifts across "
               "the frame, out of focus.",
    ),
    dict(
        name="Elder", kind="eye", side="left",
        who="an Ethiopian woman of about eighty, with the edge of a white cotton head wrap in frame",
        look="Very dark brown iris with a pale arcus; deeply lined skin with a pattern of fine "
             "creases; a few white lashes; dark thick brow touched with grey; an age spot beside "
             "the eye; a wet, thoughtful look.",
        light="Soft daylight from an open doorway; the cornea mirrors the doorway as a tall "
              "bright shape with a dark figure in it.",
        state="Looking into the lens, wise and unhurried.",
        motion="A slow, thoughtful stare. A pause. One long, slow blink. The brow lifts just "
               "perceptibly as if to say something and then does not.",
    ),
    dict(
        name="Window seat", kind="eye", side="right",
        who="a Vietnamese woman of about twenty-six",
        look="Pale tea-brown iris; neat natural brow; a faint double lid crease; a hair stuck "
             "to the cheek; fine-pored skin; a tiny pimple at the temple.",
        light="An aircraft cabin at altitude: a hard edge of bright daylight from the oval "
              "window to the right; the cornea mirrors the small oval window and a patch of "
              "cloud.",
        state="Looking into the lens with a faint curiosity.",
        motion="Her eyes drift to the window light and back to the lens. The brightness "
               "changes as the plane banks slightly. A blink. A faint widening of the eye as "
               "something outside catches her attention.",
    ),

    # ------------------------------------------------------------------- pair
    dict(
        name="Late edit", kind="pair", side="",
        who="a Persian man of about twenty-nine, with thick dark brows",
        look="Dark brown irises; thick brows nearly meeting above the nose; long lashes; a "
             "faint shadow of stubble at the cheekbones; tired eyes, a slight redness; a little "
             "dry skin on the lids.",
        light="Working at 2 a.m.: cold blue-white from a laptop below the frame; the corneas "
              "mirror a bright rectangular screen.",
        state="Both eyes on the lens, tired and focused.",
        motion="Both eyes hold the lens. Both blink, slightly out of sync. The screen's "
               "reflection flickers. A faint furrow between the brows. The eyes sharpen.",
    ),
    dict(
        name="Grey streak", kind="pair", side="",
        who="a South African Black woman of about fifty-five, with a streak of grey in her left brow",
        look="Dark brown irises with a pale arcus beginning; fine lines under the eyes; "
             "a streak of silver in one eyebrow; a slightly asymmetric lid crease; no makeup; "
             "warm brown skin with a few age spots.",
        light="Kitchen at dusk: warm light from a window plus a pendant lamp; each cornea mirrors "
              "the window and the lamp.",
        state="Both eyes on the lens, calm and warm.",
        motion="Her gaze goes from the lens to the left, as if listening to someone, and returns. "
               "Both eyes blink slowly together. One brow lifts. A little warmth comes into the "
               "eyes.",
    ),
    dict(
        name="Bleached brows", kind="pair", side="",
        who="a person of about twenty-one, East Asian, androgynous, with bleached eyebrows and a small silver ring in the left brow",
        look="Dark brown irises; the bleached brows almost white against the skin; a tiny silver "
             "ring through one brow; a very faint blue vein at the bridge; fine-pored skin; "
             "short straight lashes.",
        light="A club doorway with a hard magenta neon from the left and a cool blue from the "
              "right; the corneas mirror the two coloured light tubes.",
        state="Both eyes on the lens, cool and still.",
        motion="A slow blink in the coloured light. The neon flickers and the colour balance "
               "shifts. A faint smirk crosses the eyes. The ring catches the light.",
    ),
    dict(
        name="Pale morning", kind="pair", side="",
        who="a Swedish man of about sixty-seven",
        look="Blue irises, pale with a darker ring; white-blond brow hairs; thin, wrinkled lids; "
             "pink skin with broken capillaries on the nose bridge; glassy wet eyes; sun-damaged "
             "skin.",
        light="Flat overcast daylight outside; the corneas mirror a grey sky and a roofline.",
        state="Both eyes on the lens, steady, a little stern.",
        motion="A long, unblinking stare. Then a slow blink in unison. The wet eyes shine as the "
               "light changes. The sternness softens slightly.",
    ),
    dict(
        name="Snowfall", kind="pair", side="",
        who="an Inuit woman of about forty, with the fur trim of a parka hood framing the edges",
        look="Very dark brown irises; fine epicanthic folds; frost on a few lashes and brow "
             "hairs; weathered rosy cheeks; short thick lashes; small snow crystals on the fur.",
        light="Bright white arctic overcast; the corneas mirror a pure white sky.",
        state="Both eyes on the lens, level and warm in a freezing light.",
        motion="Snow drifts past the lens, out of focus. Frost on the lashes glitters. She "
               "blinks slowly and the frost breaks off. The gaze holds, warm.",
    ),
    dict(
        name="Cinema", kind="pair", side="",
        who="a Colombian man of about twenty-four",
        look="Brown irises; strong straight brows; fine lashes; a little shine on the lids; "
             "faint stubble at the cheekbones.",
        light="Sitting in a dark cinema: the only light is the flickering screen; the corneas "
              "mirror a bright moving film image as a rectangular glow with changing patches.",
        state="Both eyes on the lens, lit by changing light, a little amazed.",
        motion="The screen light flares and dims across the eyes. His eyes widen at something "
               "on screen, the pupils dilating, then relax. A slow blink.",
    ),
    dict(
        name="Kohl", kind="pair", side="",
        who="a Greek woman of about thirty-one with thick, nearly joined brows",
        look="Very dark brown irises; kohl liner on the waterline, a bit worn and smudged; thick "
             "natural brows; strong lashes; olive skin; one tiny gold hoop earring edge visible "
             "at the frame margin.",
        light="A table lit by a few candles at dinner; each cornea mirrors the small flame and "
              "the dark of the room.",
        state="Both eyes on the lens, an eyebrow arched.",
        motion="A slow arched brow. The candlelight flickers across the eyes. A slow blink. "
               "The gaze never leaves the lens.",
    ),
    dict(
        name="Steppe", kind="pair", side="",
        who="a Mongolian man of about fifty, weathered by wind",
        look="Dark brown irises; narrow eyes with a pronounced fold; deep squint lines; wind-"
             "chapped red skin; short thick lashes; a few grey hairs in the brow.",
        light="Open grassland in bright sun with a steady wind; the corneas mirror a huge pale "
              "sky and a distant horizon line.",
        state="Both eyes on the lens, narrowed against the wind.",
        motion="A gust moves the lashes and brow hairs and he narrows his eyes; the pupils "
               "adjust to the glare. A slow blink. The gaze stays fixed and still.",
    ),
    dict(
        name="Cat-eye frames", kind="pair", side="",
        who="an American woman of seventy-two wearing cat-eye reading glasses",
        look="Light grey-blue irises magnified slightly by the lenses; fine pale lashes; "
             "a faint line of mascara; wrinkled lids; the frame rims crossing at the edges with a "
             "tiny smudge on one lens.",
        light="Soft window light from the left, reflected in the lenses as pale rectangles "
              "that partly cover each eye.",
        state="Both eyes on the lens through the glasses, bright and a little mischievous.",
        motion="The reflection on the lenses slides as she tilts her head a hair. A slow blink "
               "behind the glasses. The eyes crinkle with a hidden smile.",
    ),
    dict(
        name="Mismatched", kind="pair", side="",
        who="a person of about thirty-five, Black and Japanese, with very curly lashes",
        look="Central heterochromia: the left iris blue-grey with a brown halo around the pupil, "
             "the right iris warm brown; very curly lashes; a slightly asymmetric brow; light "
             "brown skin with a few freckles across the nose bridge.",
        light="Bright diffused window light; the corneas mirror a pale window with a faint vertical "
              "bar of curtain.",
        state="Both eyes on the lens, curious, the head very slightly tilted.",
        motion="The head tilts a few degrees; the two eyes refocus on the lens. A slow blink. "
               "The pupils flex differently for a moment as the light shifts.",
    ),
    dict(
        name="3 a.m.", kind="pair", side="",
        who="a Pakistani man of about nineteen, a student studying through the night",
        look="Dark brown irises; red-rimmed eyes with visible capillaries; dark circles; fine "
             "peach fuzz on the brow bone; shiny skin; a small spot on the temple.",
        light="A desk lamp low to the right and a laptop glow from below; the corneas mirror "
              "the little lamp and the bright screen.",
        state="Both eyes on the lens, exhausted, lids heavy.",
        motion="Lids droop together. A heavy blink and a jerk back to wakefulness; the eyes "
               "open wider and refocus. The pupils narrow a touch in the lamp light. A small "
               "sigh visible in the lids.",
    ),
    dict(
        name="Smothered laugh", kind="pair", side="",
        who="a Filipina woman of about forty-five with fine laugh lines",
        look="Dark brown irises; crow's feet gathering at both outer corners; a trace of eyeliner; "
             "soft lids; warm brown skin; a hint of a blush on the cheekbones.",
        light="Warm tungsten lamp light from the left; the corneas mirror a warm lamp with a small "
              "shade shape.",
        state="Both eyes on the lens, bright with held-in amusement.",
        motion="She is trying not to laugh: the eyes crinkle, the lower lids lift, the gaze "
               "wavers and then returns to the lens. A quick blink. The amusement shakes the "
               "skin slightly.",
    ),
    dict(
        name="Harbour light", kind="pair", side="",
        who="a Portuguese man of eighty-three, a retired fisherman",
        look="Pale cloudy brown irises with arcus; heavy bags under the eyes; deep creases; "
             "thick white brows; sun-leathered skin with a few spots; wet watery eyes.",
        light="Sitting beside the harbour: sunlight bouncing off water throws moving caustic "
              "ripples of light across the face; the corneas mirror a bright sky and a tiny "
              "dark boat.",
        state="Both eyes on the lens, gentle and amused.",
        motion="Rippling light from the water moves across the whole face. His eyes squint "
               "gently. A slow, soft blink. The gaze is warm and unhurried.",
    ),
    dict(
        name="Headlights", kind="pair", side="",
        who="a Ghanaian woman of about twenty-eight",
        look="Very dark brown irises; natural, slightly clumped lashes; a small gold stud at "
             "the edge of the brow; smooth dark skin with a fine sheen; a faint tired "
             "redness at the lower lid.",
        light="Standing by a road at night as cars pass: sweeping white and yellow headlights "
              "flash across the face; the corneas mirror the moving sources.",
        state="Both eyes on the lens, alert.",
        motion="A pair of headlights sweeps across: the pupils contract, then slowly reopen. "
               "She blinks against the flash. The gaze holds, unfazed.",
    ),
    dict(
        name="Lazy eye", kind="pair", side="",
        who="a Brazilian man of about forty-one with a mild exotropia in his right eye",
        look="Dark brown irises; the left eye looks straight into the lens while the right eye "
             "rests outward by only a few degrees, a subtle misalignment, most of the iris still "
             "visible and the sclera not exposed more than usual; thick brows; light stubble at the very top of the cheek; "
             "creases at the corners; a natural, slightly uneven look.",
        light="Window light from the left; the corneas mirror a window; a warm bounce from a "
              "wall.",
        state="The left eye on the lens, the right eye just off.",
        motion="The left eye holds the lens; the right eye drifts slowly outward and "
               "returns. A slow blink. A tiny involuntary squint. The mismatch is natural.",
    ),
    dict(
        name="Sheer curtain", kind="pair", side="",
        who="an Indian woman of about twenty-six with a small freckle on the nose bridge",
        look="Very dark brown irises; kohl-lined waterline; strong natural brows; soft lids; "
             "warm brown skin; a tiny stud earring edge at the frame margin.",
        light="Afternoon light through a sheer curtain moved by a breeze, throwing a soft "
              "pattern of light and shade across the face; the corneas mirror the window and "
              "a bit of billowing curtain.",
        state="Both eyes on the lens, serene.",
        motion="The curtain shadow slides across the face with the breeze. Her eyes follow "
               "nothing and stay on the lens. A slow blink as the light passes.",
    ),
]

assert len(SPECS) == 50, len(SPECS)


def ident(i):
    return f"eye-{i + 1:02d}"


def frame_prompt(spec):
    fr = FRAMING[spec["kind"]].format(side=spec.get("side", ""), who=spec["who"])
    return " ".join([fr, spec["look"], spec["light"], spec["state"], RECIPE])


def kling_prompt(spec):
    return f"{spec['motion']} {KLING_CAMERA}"
