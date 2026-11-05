#!/usr/bin/env python3
"""Build kling/sheet.html (the working page for Kling) and kling/PROMPTS.md.

    kling/build_sheet.py

sheet.html shows every frame next to its motion prompt, with Copy prompt,
Download frame and a done tick (remembered in the browser), in batches of five.
Open it from Finder; it reads the frames from kling/frames/.
"""
import html
from pathlib import Path

import specs

HERE = Path(__file__).resolve().parent
BATCH = 5

SETTINGS = [
    ("Mode", "Image to Video, newest Kling model, Professional (1080p)"),
    ("Start frame", "the frame on the card (16:9, 2048 x 1152). Upload it as the first frame only"),
    ("Duration", "10 s"),
    ("Aspect ratio", "16:9"),
    ("Prompt", "the card's prompt, as is"),
    ("Negative prompt", "the one above, same for every clip"),
    ("Creativity / relevance", "toward relevance (about 0.6): small natural motion, nothing invented"),
    ("Camera movement", "none. Sound off"),
    ("Save as", "anything. Drop every mp4 into kling/raw/. They are matched back to their frame by what the first frame looks like, so names do not matter"),
]


def esc(s):
    return html.escape(s, quote=True)


def card(i, s):
    ident = specs.ident(i)
    kp = specs.kling_prompt(s)
    fp = specs.frame_prompt(s)
    return f"""
<article class="card" data-id="{ident}">
  <a class="frame" href="frames/{ident}.jpg" target="_blank" rel="noopener"><img loading="lazy" src="frames/{ident}.jpg" alt="{esc(s['name'])}"></a>
  <div class="body">
    <header><span class="num">{i + 1:02d}</span><h3>{esc(s['name'])}</h3><span class="tag">{s['kind']}</span></header>
    <p class="who">{esc(s['who'])}</p>
    <textarea readonly rows="6" spellcheck="false">{esc(kp)}</textarea>
    <div class="row">
      <button class="copy" type="button">Copy prompt</button>
      <a class="btn" href="frames/{ident}.jpg" download="{ident}.jpg">Download frame</a>
      <label class="done"><input type="checkbox"> done in Kling</label>
    </div>
    <details><summary>How the frame was made</summary><p>{esc(fp)}</p></details>
  </div>
</article>"""


def build():
    out = []
    for i, s in enumerate(specs.SPECS):
        if i % BATCH == 0:
            out.append(f'<h2 class="batch">Batch {i // BATCH + 1} <small>eyes {i + 1:02d}–{min(i + BATCH, len(specs.SPECS)):02d}</small></h2>')
        out.append(card(i, s))
    settings = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in SETTINGS)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>A EYE: Kling sheet</title>
<style>
  :root {{ --bg:#fff; --fg:#111; --mut:#666; --line:#ddd; --card:#f6f6f6; --acc:#111; --accfg:#fff; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#0b0b0b; --fg:#eee; --mut:#999; --line:#2a2a2a; --card:#151515; --acc:#eee; --accfg:#111; }} }}
  * {{ box-sizing:border-box }}
  body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.45 -apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif; }}
  main {{ max-width:1100px; margin:0 auto; padding:24px 16px 80px; }}
  h1 {{ font-size:26px; margin:0 0 4px; letter-spacing:.02em }}
  .sub {{ color:var(--mut); margin:0 0 20px }}
  .top {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px; margin-bottom:24px }}
  dl {{ display:grid; grid-template-columns:max-content 1fr; gap:6px 16px; margin:0 0 14px }}
  dt {{ color:var(--mut) }} dd {{ margin:0 }}
  .neg {{ width:100%; font:13px/1.4 ui-monospace,Menlo,monospace; }}
  .bar {{ position:sticky; top:0; z-index:5; background:var(--bg); border-bottom:1px solid var(--line); padding:10px 16px; margin:0 -16px 8px; display:flex; gap:16px; align-items:center; flex-wrap:wrap }}
  .bar b {{ font-variant-numeric:tabular-nums }}
  .bar label {{ color:var(--mut) }}
  h2.batch {{ margin:28px 0 12px; font-size:19px }} h2.batch small {{ color:var(--mut); font-weight:400; margin-left:8px }}
  .card {{ display:grid; grid-template-columns:minmax(0,1.15fr) minmax(0,1fr); gap:16px; background:var(--card); border:1px solid var(--line); border-radius:10px; padding:12px; margin-bottom:14px }}
  .card.is-done {{ opacity:.45 }}
  .card.is-hidden {{ display:none }}
  .frame img {{ width:100%; height:auto; display:block; border-radius:6px; background:#000; aspect-ratio:16/9 }}
  header {{ display:flex; align-items:baseline; gap:10px }}
  .num {{ font-variant-numeric:tabular-nums; color:var(--mut) }}
  h3 {{ margin:0; font-size:17px }}
  .tag {{ margin-left:auto; font-size:12px; color:var(--mut); border:1px solid var(--line); border-radius:99px; padding:1px 8px }}
  .who {{ color:var(--mut); margin:4px 0 8px; font-size:13px }}
  textarea {{ width:100%; resize:vertical; font:13px/1.45 ui-monospace,Menlo,monospace; background:var(--bg); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:8px }}
  .row {{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin:10px 0 }}
  button, .btn {{ font:inherit; background:var(--acc); color:var(--accfg); border:0; border-radius:6px; padding:7px 12px; cursor:pointer; text-decoration:none }}
  .btn {{ background:transparent; color:var(--fg); border:1px solid var(--line) }}
  button.ok {{ background:#1f8a4c; color:#fff }}
  .done {{ color:var(--mut); display:flex; gap:6px; align-items:center; margin-left:auto }}
  details {{ color:var(--mut); font-size:13px }} details p {{ margin:8px 0 0 }}
  @media (max-width:760px) {{ .card {{ grid-template-columns:1fr }} }}
</style></head><body><main>
<h1>A EYE: Kling sheet</h1>
<p class="sub">{len(specs.SPECS)} starting frames, one prompt each. Do them in batches of five. Batches 11 and 12 are the eccentrics.</p>
<section class="top">
  <dl>{settings}</dl>
  <p style="margin:0 0 6px;color:var(--mut)">Negative prompt (same for all):</p>
  <textarea class="neg" id="neg" readonly rows="4" spellcheck="false">{esc(specs.KLING_NEGATIVE)}</textarea>
  <div class="row"><button type="button" id="copyneg">Copy negative prompt</button></div>
</section>
<div class="bar"><span><b id="count">0</b> / {len(specs.SPECS)} done</span><label><input type="checkbox" id="hide"> hide done</label></div>
{"".join(out)}
</main>
<script>
(function () {{
  var KEY = 'aeye-kling-done', done = {{}};
  try {{ done = JSON.parse(localStorage.getItem(KEY) || '{{}}'); }} catch (e) {{}}
  function save() {{ try {{ localStorage.setItem(KEY, JSON.stringify(done)); }} catch (e) {{}} }}
  function flash(b) {{ var t = b.textContent; b.textContent = 'Copied'; b.classList.add('ok'); setTimeout(function () {{ b.textContent = t; b.classList.remove('ok'); }}, 1200); }}
  function copy(text, b) {{
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () {{ flash(b); }});
    else {{ var t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select(); document.execCommand('copy'); t.remove(); flash(b); }}
  }}
  function refresh() {{
    var n = 0, hide = document.getElementById('hide').checked;
    document.querySelectorAll('.card').forEach(function (c) {{
      var d = !!done[c.dataset.id]; if (d) n++;
      c.classList.toggle('is-done', d); c.classList.toggle('is-hidden', d && hide);
      c.querySelector('input[type=checkbox]').checked = d;
    }});
    document.getElementById('count').textContent = n;
  }}
  document.querySelectorAll('.card').forEach(function (c) {{
    c.querySelector('.copy').onclick = function () {{ copy(c.querySelector('textarea').value, this); }};
    c.querySelector('input[type=checkbox]').onchange = function () {{ done[c.dataset.id] = this.checked; if (!this.checked) delete done[c.dataset.id]; save(); refresh(); }};
  }});
  document.getElementById('copyneg').onclick = function () {{ copy(document.getElementById('neg').value, this); }};
  document.getElementById('hide').onchange = refresh;
  refresh();
}})();
</script></body></html>"""
    (HERE / "sheet.html").write_text(page)

    md = [f"# The {len(specs.SPECS)} eyes: Kling motion prompts", "",
          "Negative prompt (all clips):", "", "> " + specs.KLING_NEGATIVE, ""]
    for i, s in enumerate(specs.SPECS):
        md += [f"## {specs.ident(i)}: {s['name']} ({s['kind']})", "", f"*{s['who']}*", "",
               specs.kling_prompt(s), ""]
    (HERE / "PROMPTS.md").write_text("\n".join(md))
    print(f"wrote {HERE / 'sheet.html'} and PROMPTS.md ({len(specs.SPECS)} cards)")


if __name__ == "__main__":
    build()
