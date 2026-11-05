"""The 55 eyes.

Each spec has everything needed for two jobs:

  * the starting FRAME (made with an OpenAI image model): who, look, light, state
  * the Kling MOTION prompt (image-to-video): motion

kind:  macro = one eye fills the frame
       eye   = one eye with brow, temple and nose bridge
side:  which eye (the subject's left or right)

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
# 28 macro, 27 eye. Every frame is a single eye (the first 34 were the original run; 35-50
# were first made as both-eyes crops and redone as single eyes on request; 51-55 are the
# eccentrics, added later).

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

    # ------------------------------------------------------------ eyes 35-50
    dict(
        name="Late edit", kind="eye", side="right",
        who="a Persian man of about twenty-nine, with thick dark brows",
        look="Dark brown iris; a thick brow, the hairs growing in different directions and "
             "thickening toward the nose; long lashes; a faint shadow of stubble at the top of the "
             "cheek; a tired eye with slight redness at the waterline; a little dry skin on the lid.",
        light="Working at 2 a.m.: cold blue-white from a laptop below the frame; the cornea "
              "mirrors a bright rectangular screen.",
        state="Looking into the lens, tired and focused.",
        motion="The eye holds the lens. A blink, then another, slightly slower. The screen's "
               "reflection flickers. A faint furrow gathers in the brow. The eye sharpens.",
    ),
    dict(
        name="Grey streak", kind="eye", side="left",
        who="a South African Black woman of about fifty-five, with a streak of grey in the brow above this eye",
        look="Dark brown iris with a pale arcus beginning; fine lines under the eye; a streak of "
             "silver running through the eyebrow; a slightly uneven lid crease; no makeup; warm "
             "brown skin with a few age spots.",
        light="Kitchen at dusk: warm light from a window plus a pendant lamp; the cornea mirrors "
              "the window and the lamp.",
        state="Looking into the lens, calm and warm.",
        motion="Her gaze goes from the lens to the left, as if listening to someone, and returns. "
               "A slow blink. The brow lifts. A little warmth comes into the eye.",
    ),
    dict(
        name="Bleached brow", kind="eye", side="left",
        who="a person of about twenty-one, East Asian, androgynous, with a bleached eyebrow and a small silver ring through it",
        look="Dark brown iris; the bleached brow almost white against the skin; a tiny silver ring "
             "through the brow; a very faint blue vein at the bridge of the nose; fine-pored skin; "
             "short straight lashes.",
        light="A club doorway with a hard magenta neon from the left and a cool blue from the "
              "right; the cornea mirrors the two coloured light tubes.",
        state="Looking into the lens, cool and still.",
        motion="A slow blink in the coloured light. The neon flickers and the colour balance "
               "shifts. A faint smirk crosses the eye. The ring catches the light.",
    ),
    dict(
        name="Steel grey", kind="macro", side="right",
        who="a Latvian man of about sixty-seven",
        look="Steel-grey iris with a rust-brown ring around the pupil and fine pale radial "
             "fibres; white-blond brow hairs; thin, wrinkled lids; pink skin with broken capillaries; "
             "a glassy wet eye; sun-damaged skin.",
        light="Flat overcast daylight outside; the cornea mirrors a grey sky and a roofline.",
        state="Looking into the lens, steady, a little stern.",
        motion="A long, unblinking stare. Then a slow blink. The wet eye shines as the light "
               "changes. The sternness softens slightly.",
    ),
    dict(
        name="Snowfall", kind="eye", side="right",
        who="an Inuit woman of about forty, with the fur trim of a parka hood framing the edge of the picture",
        look="Very dark brown iris; a fine epicanthic fold; frost on a few lashes and brow hairs; "
             "weathered rosy cheek; short thick lashes; small snow crystals on the fur.",
        light="Bright white arctic overcast; the cornea mirrors a pure white sky.",
        state="Looking into the lens, level and warm in a freezing light.",
        motion="Snow drifts past the lens, out of focus. Frost on the lashes glitters. She blinks "
               "slowly and a little frost breaks off. The gaze holds, warm.",
    ),
    dict(
        name="Cinema", kind="macro", side="left",
        who="a Colombian man of about twenty-four",
        look="Brown iris; a strong straight brow; fine lashes; a little shine on the lid; a faint "
             "shadow of stubble at the top of the cheek.",
        light="Sitting in a dark cinema: the only light is the flickering screen; the cornea "
              "mirrors a bright moving film image as a rectangular glow with changing patches.",
        state="Looking into the lens, lit by changing light, a little amazed.",
        motion="The screen light flares and dims across the eye. His eye widens at something on "
               "screen, the pupil dilating, then relaxes. A slow blink.",
    ),
    dict(
        name="Bare bulb", kind="macro", side="left",
        who="a Greek woman of about thirty-one with a thick, strongly arched brow",
        look="Very dark brown iris; kohl liner on the waterline, a bit worn and smudged; a thick "
             "natural brow; strong lashes; olive skin.",
        light="A night street market lit by a single bare tungsten bulb hanging above and in "
              "front of her; the cornea mirrors the bare bulb and the dark edge of an awning.",
        state="Looking into the lens, the brow arched.",
        motion="The bulb sways a little in the wind and its reflection slides across the cornea. "
               "A slow arch of the brow. A slow blink. The gaze never leaves the lens.",
    ),
    dict(
        name="Steppe", kind="eye", side="left",
        who="a Mongolian man of about fifty, weathered by wind",
        look="Dark brown iris; a narrow eye with a pronounced fold; deep squint lines; wind-chapped "
             "red skin; short thick lashes; a few grey hairs in the brow.",
        light="Open grassland in bright sun with a steady wind; the cornea mirrors a huge pale "
              "sky and a distant horizon line.",
        state="Looking into the lens, narrowed against the wind.",
        motion="A gust moves the lashes and brow hairs and he narrows his eye; the pupil adjusts "
               "to the glare. A slow blink. The gaze stays fixed and still.",
    ),
    dict(
        name="Cat-eye frames", kind="eye", side="right",
        who="an American woman of seventy-two wearing cat-eye reading glasses",
        look="Light grey-blue iris, magnified slightly by the lens; fine pale lashes; a faint line "
             "of mascara; a wrinkled lid; the tortoiseshell frame crossing the edge of the picture, "
             "a tiny smudge on the lens.",
        light="Soft window light from the left, reflected in the lens as a pale rectangle that "
              "partly covers the eye.",
        state="Looking into the lens through the glasses, bright and a little mischievous.",
        motion="The reflection on the lens slides as she tilts her head a hair. A slow blink "
               "behind the glasses. The eye crinkles with a hidden smile.",
    ),
    dict(
        name="Halo", kind="macro", side="left",
        who="a person of about thirty-five, Black and Japanese, with very curly lashes",
        look="Central heterochromia: a blue-grey iris with a distinct warm brown halo around the "
             "pupil, its boundary jagged and feathered; very curly lashes; a slightly uneven brow; "
             "light brown skin with a few freckles.",
        light="Bright diffused window light; the cornea mirrors a pale window with a faint "
              "vertical bar of curtain.",
        state="Looking into the lens, curious, the head very slightly tilted.",
        motion="The head tilts a few degrees and the eye refocuses on the lens. A slow blink. "
               "The pupil flexes and the brown halo seems to shift as the light moves.",
    ),
    dict(
        name="3 a.m.", kind="macro", side="right",
        who="a Pakistani man of about nineteen, a student studying through the night",
        look="Dark brown iris; a faintly pink waterline and a few fine red capillaries on the sclera, tired but not bloodshot, not inflamed; a dark circle beneath; "
             "fine peach fuzz on the brow bone; shiny skin; a small spot at the temple.",
        light="A desk lamp low to the right and a laptop glow from below; the cornea mirrors the "
              "little lamp and the bright screen.",
        state="Looking into the lens, exhausted, the lid heavy.",
        motion="The lid droops. A heavy blink and a jerk back to wakefulness; the eye opens wider "
               "and refocuses. The pupil narrows a touch in the lamp light. A small sigh shows "
               "in the lid.",
    ),
    dict(
        name="Smothered laugh", kind="eye", side="left",
        who="a Thai woman of about forty-five with fine laugh lines",
        look="Dark brown iris; crow's feet gathering at the outer corner; a trace of eyeliner; a "
             "soft lid; warm brown skin; a hint of a blush on the cheekbone.",
        light="Warm tungsten lamp light from the left; the cornea mirrors a warm lamp with a small "
              "shade shape.",
        state="Looking into the lens, bright with held-in amusement.",
        motion="She is trying not to laugh: the eye crinkles, the lower lid lifts, the gaze wavers "
               "and then returns to the lens. A quick blink. The amusement shakes the skin slightly.",
    ),
    dict(
        name="Harbour light", kind="eye", side="right",
        who="a Portuguese man of eighty-three, a retired fisherman",
        look="Pale cloudy brown iris with arcus; heavy bags under the eye; deep creases; a thick "
             "white brow; sun-leathered skin with a few spots; a watery eye.",
        light="Sitting beside the harbour: sunlight bouncing off water throws moving caustic "
              "ripples of light across the face; the cornea mirrors a bright sky and a tiny dark boat.",
        state="Looking into the lens, gentle and amused.",
        motion="Rippling light from the water moves across the whole face. His eye squints "
               "gently. A slow, soft blink. The gaze is warm and unhurried.",
    ),
    dict(
        name="Headlights", kind="macro", side="left",
        who="a Ghanaian woman of about twenty-eight",
        look="Very dark brown iris; natural, slightly clumped lashes; a small gold stud at the end "
             "of the brow; smooth dark skin with a fine sheen; a faint tired redness at the lower lid.",
        light="Standing by a road at night as cars pass: sweeping white and yellow headlights flash "
              "across the face; the cornea mirrors the moving sources.",
        state="Looking into the lens, alert.",
        motion="A pair of headlights sweeps across: the pupil contracts, then slowly reopens. She "
               "blinks against the flash. The gaze holds, unfazed.",
    ),
    dict(
        name="Iris freckle", kind="macro", side="right",
        who="a Brazilian man of about forty-one",
        look="Dark brown iris with one tiny dark freckle (an iris naevus) near the edge at about "
             "seven o'clock, and a faint pale pinguecula on the nasal sclera; a thick brow; light "
             "stubble shadow at the very top of the cheek; creases at the corner; a natural, "
             "slightly uneven look.",
        light="Window light from the left; the cornea mirrors a window; a warm bounce from a wall.",
        state="Looking into the lens, relaxed.",
        motion="A steady gaze. The pupil breathes with the light and the dark freckle on the iris "
               "drifts with it. A slow blink. A tiny involuntary squint.",
    ),
    dict(
        name="Sheer curtain", kind="eye", side="left",
        who="an Indian woman of about twenty-six with a small freckle on the nose bridge",
        look="Very dark brown iris; kohl-lined waterline; a strong natural brow; a soft lid; warm "
             "brown skin.",
        light="Afternoon light through a sheer curtain moved by a breeze, throwing a soft pattern "
              "of light and shade across the face; the cornea mirrors the window and a bit of "
              "billowing curtain.",
        state="Looking into the lens, serene.",
        motion="The curtain shadow slides across the face with the breeze. Her eye follows "
               "nothing and stays on the lens. A slow blink as the light passes.",
    ),
    # ------------------------------------------------- eyes 51-55: the eccentrics
    # People defined by what they do, with something physically in front of or on the eye.
    dict(
        name="Loupe", kind="eye", side="right",
        who="a Swiss watchmaker of about seventy-one with enormous wild white eyebrows",
        look="A jeweller's loupe screwed into the eye socket: its brass and black barrel fills the "
             "edges of the picture and its lens magnifies the pale blue-grey iris and the lids behind "
             "it, softening and slightly bending the periphery; thin pale lashes; liver spots on the "
             "lid; white eyebrow hairs as long as fingers, some curling forward; deep furrows from a "
             "lifetime of squinting; a few tiny brass filings on the skin.",
        light="A bright adjustable bench lamp from the upper left; the front of the loupe mirrors it "
              "as a hard oval highlight with a faint reflection of a watch movement on a dark bench; "
              "a pinpoint of the lamp in the cornea.",
        state="Looking into the lens through the loupe, absorbed, as if interrupted at his work.",
        motion="He holds still, absorbed, then slowly lifts his gaze from the work to the lens, the "
               "magnified iris sliding behind the glass. The pupil adjusts. A slow blink behind the "
               "loupe, the brow lowering to grip it in place. A tiny tremor in the old hand's "
               "shadow.",
    ),
    dict(
        name="Veil", kind="eye", side="left",
        who="a Slovenian beekeeper of about fifty-eight",
        look="Seen through the fine black mesh of a beekeeper's veil: the mesh is a soft dark grid "
             "in front of the lens, out of focus, except for one honeybee crawling on it, sharp, just "
             "in front of the eye; hazel-green iris; sun-weathered skin with a faint amber propolis "
             "stain on the cheek; a wisp of grey hair escaping under the veil; a drop of sweat at the "
             "temple; a second bee walking on the brow.",
        light="Bright summer meadow at midday, sun above and behind her, a thin thread of smoke "
              "drifting past; the cornea mirrors a white sky and the dark shape of a stacked hive box.",
        state="Looking into the lens through the mesh, calm and unhurried, not afraid of the bees.",
        motion="The bee crawls slowly across the mesh and takes off, a blur. A thread of smoke "
               "drifts across the eye. She blinks slowly through the veil, calm. The pupil adjusts "
               "to a patch of sun.",
    ),
    dict(
        name="Greasepaint", kind="eye", side="right",
        who="a Black man of about fifty-five, a retired circus clown still in half make-up",
        look="White greasepaint cracked in the creases of the lid and the crow's feet; a black "
             "diamond painted over the brow and lid, worn and smeared; the start of a thick painted "
             "red arc at the bottom edge of the picture; the paint shiny with sweat and streaked "
             "below the eye; dark brown iris, red-rimmed and tired; real eyebrow hairs poking through "
             "the white; a little greasepaint caught on the lashes.",
        light="Backstage: a dressing-room mirror ringed with bare bulbs; the cornea mirrors a row of "
              "small round bulbs; warm hard light from the left.",
        state="Looking into the lens, tired and dignified, between shows.",
        motion="He holds the gaze, still and tired. A slow blink that cracks the paint at the lid. "
               "The brow lifts a little and a flake of white drops. The bulbs flicker faintly. His "
               "eye softens.",
    ),
    dict(
        name="Eyepiece", kind="eye", side="left",
        who="an amateur astronomer in her mid thirties, Nigerian-British, with electric-blue dyed eyebrows growing out at the roots",
        look="Her eye held a few centimetres from the black rubber eyecup of a telescope eyepiece, "
             "which fills the lower right corner of the picture with a little of its metal barrel; "
             "dark brown iris with the pupil opened wide in the dark; the blue brow dye patchy; "
             "dew beaded on her lashes from the night air; her skin faintly ringed where the "
             "rubber pressed it.",
        light="A cold damp field at night: the only light is a dim red torch from below and to the "
              "right, turning the skin deep red; the cornea mirrors a tiny bright disc of a planet "
              "and one point of the red torch.",
        state="Looking up into the lens from the eyepiece, as if the lens were the planet.",
        motion="The pupil stays wide; the tiny bright disc in the cornea wobbles and dims as the "
               "planet drifts. She lifts her eye from the eyepiece to the lens. A slow blink; dew "
               "shakes from the lashes. Her breath fogs the rubber cup.",
    ),
    dict(
        name="Furnace", kind="macro", side="right",
        who="a Czech glassblower of about forty-five, a woman with a singed eyebrow",
        look="Safety glasses pushed up onto the forehead, only their top rim visible; pale "
             "grey-green iris; part of the eyebrow singed short and curled; a streak of soot on the "
             "cheekbone; sweat running in the creases; the skin flushed and shiny; short sun-bleached "
             "lashes, a few curled by heat; fine ash on the lid.",
        light="Standing in front of the open glory-hole of a furnace: intense orange-white light "
              "from the left, the other side of the face in deep shadow; the cornea mirrors a small "
              "bright orange circle with a glowing gob of glass on a pipe in it; visible heat shimmer.",
        state="Looking into the lens with a squint against the heat.",
        motion="Heat shimmer ripples the air in front of the face. The orange glow pulses; the "
               "pupil pinches small and opens as the glow fades. She squints harder, then relaxes, a "
               "bead of sweat running into the corner of the eye. A slow blink.",
    ),
]

assert len(SPECS) == 55, len(SPECS)


def ident(i):
    return f"eye-{i + 1:02d}"


def frame_prompt(spec):
    fr = FRAMING[spec["kind"]].format(side=spec.get("side", ""), who=spec["who"])
    return " ".join([fr, spec["look"], spec["light"], spec["state"], RECIPE])


def kling_prompt(spec):
    return f"{spec['motion']} {KLING_CAMERA}"
