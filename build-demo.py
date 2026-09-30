#!/usr/bin/env python3
"""Build the France wipe-slider demo page (Jason D's Vision, 2026-09-30).

Standalone demo: first 3 France scenes with the day/night wipe slider.
Night base (newly generated) vs day overlay (existing France masters).
NOT the builder's repo — a separate demo repo so the builder's index.html
and durable generator are untouched.
"""
import os

SITE = os.path.dirname(os.path.abspath(__file__))

SCENES = [
    {"id": "FR-01-001", "slug": "fr-01-001", "caption": "Eiffel Tower, Paris",
     "desc": "The tower centered from the Champ de Mars, floodlit gold against the night sky."},
    {"id": "FR-01-002", "slug": "fr-01-002", "caption": "Louvre Pyramid, Paris",
     "desc": "The glowing pyramid mirrored in the Cour Napoleon reflecting pool at night."},
    {"id": "FR-01-003", "slug": "fr-01-003", "caption": "Notre-Dame Cathedral, Paris",
     "desc": "The west front and rose window floodlit over the parvis at night."},
]

WIPE_CSS = open("/tmp/fr_wipe/WIPE_CSS.css").read()

PAGE_CSS = """
  * { box-sizing: border-box; }
  body { margin: 0; background: #141210; color: #f2ede3;
         font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  .flag-stripe { height: 10px;
    background: linear-gradient(90deg, #0055a4 0 33.3%, #ffffff 33.3% 66.6%, #ef4135 66.6% 100%); }
  header { max-width: 1100px; margin: 0 auto; padding: 28px 20px 8px; }
  header h1 { margin: 0 0 6px; font-size: 28px; }
  header p { margin: 0; color: #b9b2a4; font-size: 15px; }
  header .demo-note { display: inline-block; margin-top: 10px; font-size: 13px;
    color: #f2ede3; background: #2a2620; border: 1px solid #4a443a;
    padding: 6px 12px; border-radius: 20px; }
  .grid { max-width: 1100px; margin: 0 auto; padding: 20px;
          display: grid; gap: 28px; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
  .card { background: #1d1a16; border: 1px solid #35302a; border-radius: 12px;
          overflow: hidden; }
  .preview { position: relative; width: 100%; aspect-ratio: 16 / 9; background: #000; }
  .preview.r45 { aspect-ratio: 4 / 5; }
  .preview img.base { position: absolute; inset: 0; width: 100%; height: 100%;
                      object-fit: cover; display: block; }
  .fmt-tabs { display: flex; gap: 8px; padding: 12px 14px 0; }
  .fmt-tab { border: 1px solid #4a443a; background: #2a2620; color: #f2ede3;
             border-radius: 8px; padding: 6px 12px; font-size: 13px; cursor: pointer; }
  .fmt-tab.is-active { background: #f2ede3; color: #141210; font-weight: 700; }
  .card h3 { margin: 12px 14px 4px; font-size: 18px; }
  .card .desc { margin: 0 14px 16px; color: #b9b2a4; font-size: 14px; line-height: 1.45; }
  footer { max-width: 1100px; margin: 0 auto; padding: 8px 20px 40px;
           color: #8a8378; font-size: 13px; }
"""

WIPE_JS = """
document.querySelectorAll('.card').forEach(function(card) {
  var wipe = card.querySelector('.wipe');
  var wipeDay = wipe.querySelector('.wipe-day');
  var wipeHandle = wipe.querySelector('.wipe-handle');
  var wipeDivider = wipe.querySelector('.wipe-divider');
  var base = card.querySelector('img.base');
  var preview = card.querySelector('.preview');
  var wipePos = 50;
  function fmt() {
    var t = card.querySelector('.fmt-tab.is-active');
    return t ? t.getAttribute('data-format') : '16x9';
  }
  function wipeSet(p) {
    wipePos = Math.max(0, Math.min(100, p));
    wipeDivider.style.left = wipePos + '%';
    wipeDay.style.clipPath = 'inset(0 0 0 ' + wipePos + '%)';
    wipeHandle.style.left = wipePos + '%';
    wipeHandle.setAttribute('aria-valuenow', String(Math.round(wipePos)));
  }
  function wipeActivate() {
    if (wipeDay.getAttribute('src')) return;
    var key = fmt() === '4x5' ? 'data-src-45-day' : 'data-src-16-day';
    var s = wipeDay.getAttribute(key);
    if (s) wipeDay.setAttribute('src', s);
  }
  wipeHandle.addEventListener('pointerdown', function(e) {
    e.preventDefault();
    wipeActivate();
    try { wipeHandle.setPointerCapture(e.pointerId); } catch (err) {}
    var r = wipe.getBoundingClientRect();
    var move = function(ev) { if (r.width > 0) wipeSet((ev.clientX - r.left) / r.width * 100); };
    var up = function() {
      wipeHandle.removeEventListener('pointermove', move);
      wipeHandle.removeEventListener('pointerup', up);
      wipeHandle.removeEventListener('pointercancel', up);
    };
    wipeHandle.addEventListener('pointermove', move);
    wipeHandle.addEventListener('pointerup', up);
    wipeHandle.addEventListener('pointercancel', up);
  });
  wipeHandle.addEventListener('click', function(e) { e.stopPropagation(); });
  wipeHandle.addEventListener('keydown', function(e) {
    var step = e.shiftKey ? 10 : 3, handled = true;
    if (e.key === 'ArrowLeft') wipeSet(wipePos - step);
    else if (e.key === 'ArrowRight') wipeSet(wipePos + step);
    else if (e.key === 'Home') wipeSet(0);
    else if (e.key === 'End') wipeSet(100);
    else handled = false;
    if (handled) { e.preventDefault(); wipeActivate(); }
  });
  card.querySelectorAll('.fmt-tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
      card.querySelectorAll('.fmt-tab').forEach(function(t) { t.classList.remove('is-active'); });
      tab.classList.add('is-active');
      var f = tab.getAttribute('data-format');
      base.setAttribute('src', base.getAttribute(f === '4x5' ? 'data-src-45' : 'data-src-16'));
      preview.classList.toggle('r45', f === '4x5');
      if (wipeDay.getAttribute('src'))
        wipeDay.setAttribute('src', wipeDay.getAttribute(f === '4x5' ? 'data-src-45-day' : 'data-src-16-day'));
      wipeSet(wipePos);
    });
  });
  wipeSet(50);
});
"""


def card_html(s):
    slug = s["slug"]
    return f"""
    <article class="card">
      <div class="preview">
        <img class="base" src="assets/{slug}-night-16x9.png"
             data-src-16="assets/{slug}-night-16x9.png"
             data-src-45="assets/{slug}-night-4x5.png"
             alt="AI-generated artistic interpretation of {s['caption']} at night">
        <div class="wipe">
          <img class="wipe-day" data-src-16-day="assets/{slug}-day-16x9.png"
               data-src-45-day="assets/{slug}-day-4x5.png"
               alt="" aria-hidden="true" style="clip-path: inset(0 0 0 50%);">
          <div class="wipe-divider" style="left: 50%;"></div>
          <button type="button" class="wipe-handle" style="left: 50%;" role="slider"
                  aria-label="Drag to compare night and day views of {s['caption']}"
                  aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">&#8596;</button>
          <span class="wipe-label wipe-label-night">&#9790; night</span>
          <span class="wipe-label wipe-label-day">day &#9728;</span>
        </div>
      </div>
      <div class="fmt-tabs">
        <button type="button" class="fmt-tab is-active" data-format="16x9">16:9</button>
        <button type="button" class="fmt-tab" data-format="4x5">4:5</button>
      </div>
      <h3>{s['caption']}</h3>
      <p class="desc">{s['desc']}</p>
    </article>"""


html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>France wipe-slider demo &middot; Jason D's Vision</title>
<style>{PAGE_CSS}{WIPE_CSS}</style>
</head>
<body>
<div class="flag-stripe"></div>
<header>
  <h1>France &middot; day/night wipe slider demo</h1>
  <p>Drag the handle on any card to wipe between the night and day views of the same viewpoint.</p>
  <span class="demo-note">Demo &mdash; first 3 France scenes &middot; not yet on the live France gallery</span>
</header>
<main class="grid">
{''.join(card_html(s) for s in SCENES)}
</main>
<footer>Jason D's Vision &middot; AI-generated artistic interpretations &middot; Not photographs.</footer>
<script>{WIPE_JS}</script>
</body>
</html>
"""

out = os.path.join(SITE, "index.html")
open(out, "w").write(html)
print("wrote", out, len(html), "bytes")
