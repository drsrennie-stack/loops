#!/usr/bin/env python3
"""Build the HTML slide show, the version that runs on the projector.

Same 52 questions, same order, same key. What is different from the practice
exam page is who is driving. The exam page is a student typing answers at a
laptop. This is Dr. Rennie at the front of a room with a clicker, so it fills
the screen, the type is sized for the back row, nothing is typed into it, and
the answers stay hidden until she presses A.

One file. Every picture is a data URI, so it projects from a memory stick, a
borrowed laptop or a classroom with no wifi.
"""
import base64
import io
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data  # noqa: E402

OUT = '/root/t3/out'
PICS = os.path.join(OUT, 'images/module1-practice')
WIDTH = 1000


def uri(stem):
    im = Image.open(os.path.join(PICS, stem + '.jpg')).convert('RGB')
    if im.width > WIDTH:
        im = im.resize((WIDTH, round(im.height * WIDTH / im.width)),
                       Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=82, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def build():
    slides = []
    for stem, qs in data.slides():
        slides.append({
            's': stem,
            'qs': [{'n': q['n'], 'tag': q['tag'], 'a': q['a'],
                    'alt': q.get('alt', [])} for q in qs],
        })
    pics = {st: uri(st) for st in sorted({s['s'] for s in slides})}

    payload = json.dumps({
        'title': data.TITLE, 'course': data.COURSE, 'school': data.SCHOOL,
        'byline': data.BYLINE, 'slides': slides, 'pics': pics,
    }, ensure_ascii=False, separators=(',', ':'))

    html = TEMPLATE.replace('/*DATA*/', 'var D = ' + payload + ';')
    path = os.path.join(OUT, 'module1-slideshow.html')
    open(path, 'w', encoding='utf-8').write(html)
    print('slide show: %d slides, %d questions, %.1f MB'
          % (len(slides), len(data.QUESTIONS), os.path.getsize(path) / 1e6))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Module 1 Practice Lab Exam | Slide show</title>
<meta name="description" content="Projector slide show for the BIO 004 Module 1 practice lab exam. Ninety seconds a slide, answers on demand.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#1E3D4C; --navy-deep:#142a36; --navy-tint:#EDF1F3;
  --gold:#B8924A; --terra:#8B3A2E;
  --white:#fff; --off:#FAFAF9; --line:#D7DDE0; --muted:#465660;
  --good:#1F5B3A;
  --fd:"Plus Jakarta Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --fb:"DM Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--white);color:var(--navy);font-family:var(--fb);
  font-size:17px;line-height:1.5;overflow:hidden}
img{max-width:100%;display:block}
:focus-visible{outline:3px solid var(--navy);outline-offset:3px;border-radius:4px;
  box-shadow:0 0 0 6px rgba(184,146,74,.45)}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0 0 0 0);white-space:nowrap;border:0}

.stage{display:flex;flex-direction:column;height:100%}

/* ---------- top strip ---------- */
.top{display:flex;align-items:center;gap:16px;padding:14px clamp(20px,3vw,48px) 0}
.eyebrow{font-family:var(--fb);font-size:clamp(11px,1.1vw,14px);font-weight:700;
  letter-spacing:.09em;text-transform:uppercase;color:var(--terra);margin:0}
.spacer{margin-left:auto}
.clock{font-family:var(--fd);font-weight:800;font-variant-numeric:tabular-nums;
  font-size:clamp(1.1rem,2vw,1.6rem);min-width:3.6ch;text-align:right}
.clock.low{color:var(--terra)}
.counter{font-family:var(--fd);font-weight:700;color:var(--muted);
  font-size:clamp(.85rem,1.3vw,1.05rem)}
.bar{height:8px;background:var(--navy-tint);border-radius:999px;overflow:hidden;
  margin:10px clamp(20px,3vw,48px) 0}
.bar span{display:block;height:100%;width:100%;background:var(--gold)}
@media (prefers-reduced-motion: no-preference){.bar span{transition:width 300ms linear}}
.paused .bar span{background:var(--muted)}

/* ---------- the slide ---------- */
.slide{flex:1;min-height:0;display:grid;gap:clamp(20px,3vw,48px);
  grid-template-columns:minmax(0,0.9fr) minmax(0,1.1fr);
  align-items:center;padding:clamp(14px,2vh,28px) clamp(20px,3vw,48px)}
.slide.title{grid-template-columns:1fr}
@media (max-width:900px){.slide{grid-template-columns:1fr;align-items:start;overflow:auto}}

.qblock{margin:0 0 clamp(20px,3.4vh,44px)}
.qblock:last-child{margin-bottom:0}
.qline{display:flex;gap:.5em;align-items:baseline}
.qn{font-family:var(--fd);font-weight:800;color:var(--terra);
  font-size:clamp(1.4rem,2.9vw,2.5rem);line-height:1.12}
.qtag{font-family:var(--fd);font-weight:600;color:var(--navy);
  font-size:clamp(1.3rem,2.6vw,2.3rem);line-height:1.18;margin:0}
.ans{margin:.5em 0 0 0;font-family:var(--fd);font-weight:700;color:var(--good);
  font-size:clamp(1rem,1.9vw,1.6rem);line-height:1.25}
.altline{margin:.25em 0 0;color:var(--muted);font-size:clamp(.8rem,1.1vw,1rem)}
.ansbox[hidden]{display:none}

.plate{height:100%;display:flex;align-items:center;justify-content:center}
.plate img{max-height:100%;max-width:100%;width:auto;height:auto;object-fit:contain;
  border:1px solid var(--line);border-radius:8px}

h1{font-family:var(--fd);font-weight:800;font-size:clamp(2.4rem,6vw,5rem);
  line-height:1.06;margin:.2em 0 .3em}
.lede{font-size:clamp(1.05rem,1.9vw,1.6rem);color:var(--muted);margin:0 0 .5em;max-width:36ch}
.byline{font-family:var(--fd);font-weight:600;font-size:clamp(1rem,1.5vw,1.3rem);
  margin-top:2.2em}
kbd{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.85em;
  border:1px solid var(--line);border-bottom-width:2px;border-radius:5px;padding:1px 6px;
  background:var(--off)}

/* ---------- bottom controls ---------- */
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  padding:0 clamp(20px,3vw,48px) 16px}
.btn{font-family:var(--fd);font-weight:700;font-size:.95rem;border-radius:9px;
  padding:11px 18px;min-height:44px;cursor:pointer;border:1px solid var(--navy);
  background:var(--white);color:var(--navy)}
.btn:hover{background:var(--navy-tint)}
.btn.solid{background:var(--navy);color:#fff}
.btn.solid:hover{background:var(--navy-deep)}
.btn[aria-pressed="true"]{background:var(--navy);color:#fff}
.hint{color:var(--muted);font-size:.86rem}
@media (max-width:900px){.hint{display:none}}
</style>
</head>
<body>
<div class="stage">

  <div class="top">
    <p class="eyebrow" id="eyebrow"></p>
    <span class="spacer"></span>
    <span class="counter" id="counter"></span>
    <span class="clock" id="clock">1:30</span>
  </div>
  <div class="bar" id="barWrap"><span id="bar"></span></div>

  <main class="slide" id="slide" aria-live="off"></main>

  <div class="controls">
    <button class="btn" id="prev" type="button">Back</button>
    <button class="btn solid" id="next" type="button">Next</button>
    <button class="btn" id="answers" type="button" aria-pressed="false">Show the answers</button>
    <button class="btn" id="pause" type="button" aria-pressed="false">Pause</button>
    <button class="btn" id="full" type="button">Full screen</button>
    <button class="btn" id="clockBtn" type="button">Clock: 1:30</button>
    <span class="hint"><kbd>&rarr;</kbd> next &nbsp; <kbd>&larr;</kbd> back &nbsp;
      <kbd>A</kbd> answers &nbsp; <kbd>P</kbd> pause &nbsp; <kbd>F</kbd> full screen</span>
  </div>
</div>
<p class="sr" id="live" role="status" aria-live="polite"></p>

<script>
"use strict";
/*DATA*/

var CLOCKS = [90, 60, 75, 120, 0];
var clockIx = 0, secs = CLOCKS[0];
var at = -1;                  // -1 is the title slide
var left = 0, tick = null, paused = false, showing = false;

var el = function(id){ return document.getElementById(id); };
function esc(s){
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}
function label(n){ return n ? (Math.floor(n/60) + ":" + (n%60<10?"0":"") + (n%60)) : "No timer"; }

function paint(){
  var slide = el("slide");
  showing = false;
  el("answers").setAttribute("aria-pressed", "false");
  el("answers").textContent = "Show the answers";

  if (at < 0){
    el("eyebrow").textContent = D.course + "  ·  " + D.school;
    el("counter").textContent = "";
    slide.className = "slide title";
    slide.innerHTML =
      "<div><h1>" + esc(D.title) + "</h1>"
      + '<p class="lede">Two questions on every slide. '
      + (secs ? label(secs).replace(":", " minute ") + " on each." : "No clock.")
      + '</p>'
      + '<p class="lede">Answer on your sheet by number. The slide moves on without you.</p>'
      + '<p class="byline">' + esc(D.byline) + "</p></div>";
    stopClock();
    el("clock").textContent = label(secs);
    el("bar").style.width = "100%";
    el("live").textContent = D.title + ". Press the right arrow to begin.";
    return;
  }

  var s = D.slides[at];
  el("eyebrow").textContent = D.course + "  ·  Module 1 Practice";
  el("counter").textContent = "Slide " + (at + 1) + " of " + D.slides.length
    + "   ·   Questions " + s.qs[0].n + " and " + s.qs[s.qs.length - 1].n;
  slide.className = "slide";

  var left_col = s.qs.map(function(q){
    return '<div class="qblock">'
      + '<div class="qline"><span class="qn">' + q.n + '.</span>'
      + '<p class="qtag">' + esc(q.tag) + "</p></div>"
      + '<div class="ansbox" hidden>'
      + '<p class="ans">' + esc(q.a) + "</p>"
      + (q.alt && q.alt.length
          ? '<p class="altline">Also accepted: ' + esc(q.alt.join(", ")) + "</p>" : "")
      + "</div></div>";
  }).join("");

  slide.innerHTML = "<div>" + left_col + "</div>"
    + '<div class="plate"><img src="' + D.pics[s.s] + '" alt="Specimen for questions '
    + s.qs[0].n + " and " + s.qs[s.qs.length - 1].n
    + '. Identify it by eye from the slide."></div>';

  el("prev").disabled = false;
  el("live").textContent = "Slide " + (at + 1) + ". Question " + s.qs[0].n + ", "
    + s.qs[0].tag + ". Question " + s.qs[s.qs.length - 1].n + ", "
    + s.qs[s.qs.length - 1].tag + ".";
  startClock();
}

function startClock(){
  stopClock();
  if (!secs){
    el("clock").textContent = "No timer";
    el("clock").classList.remove("low");
    el("bar").style.width = "100%";
    return;
  }
  left = secs;
  drawClock();
  tick = setInterval(function(){
    if (paused) return;
    left--;
    drawClock();
    if (left === 30 || left === 10) el("live").textContent = left + " seconds left.";
    if (left <= 0){ stopClock(); go(1, true); }
  }, 1000);
}
function drawClock(){
  el("clock").textContent = label(left);
  el("clock").classList.toggle("low", left <= 15);
  el("bar").style.width = Math.max(0, (left / secs) * 100) + "%";
}
function stopClock(){ if (tick){ clearInterval(tick); tick = null; } }

function go(d, auto){
  var n = at + d;
  if (n < -1) return;
  if (n >= D.slides.length){
    if (auto) { stopClock(); el("live").textContent = "That was the last slide."; }
    return;
  }
  at = n;
  paint();
}

function toggleAnswers(){
  if (at < 0) return;
  showing = !showing;
  Array.prototype.forEach.call(document.querySelectorAll(".ansbox"), function(b){
    b.hidden = !showing;
  });
  var b = el("answers");
  b.setAttribute("aria-pressed", String(showing));
  b.textContent = showing ? "Hide the answers" : "Show the answers";
  el("live").textContent = showing ? "Answers showing." : "Answers hidden.";
}
function togglePause(){
  if (!secs || at < 0) return;
  paused = !paused;
  var b = el("pause");
  b.setAttribute("aria-pressed", String(paused));
  b.textContent = paused ? "Resume" : "Pause";
  document.body.classList.toggle("paused", paused);
  el("live").textContent = paused ? "Clock paused." : "Clock running.";
}
function fullscreen(){
  if (document.fullscreenElement) document.exitFullscreen();
  else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
}
function cycleClock(){
  clockIx = (clockIx + 1) % CLOCKS.length;
  secs = CLOCKS[clockIx];
  el("clockBtn").textContent = "Clock: " + label(secs);
  el("live").textContent = "Clock set to " + label(secs) + ".";
  if (at >= 0) startClock(); else el("clock").textContent = label(secs);
}

el("next").addEventListener("click", function(){ go(1); });
el("prev").addEventListener("click", function(){ go(-1); });
el("answers").addEventListener("click", toggleAnswers);
el("pause").addEventListener("click", togglePause);
el("full").addEventListener("click", fullscreen);
el("clockBtn").addEventListener("click", cycleClock);

document.addEventListener("keydown", function(e){
  var a = document.activeElement;
  var onButton = a && a.tagName.toLowerCase() === "button";
  switch (e.key){
    case "ArrowRight": case "PageDown": e.preventDefault(); go(1); break;
    case "ArrowLeft": case "PageUp": e.preventDefault(); go(-1); break;
    case " ": case "Enter":
      /* Space and Enter are how a keyboard user presses the button they have
         tabbed to, so they only advance the deck when focus is elsewhere. */
      if (onButton) return;
      e.preventDefault(); go(1); break;
    case "Home": e.preventDefault(); at = -1; paint(); break;
    case "End": e.preventDefault(); at = D.slides.length - 1; paint(); break;
    case "a": case "A": toggleAnswers(); break;
    case "p": case "P": togglePause(); break;
    case "f": case "F": fullscreen(); break;
  }
});

el("clockBtn").textContent = "Clock: " + label(secs);
paint();
</script>
</body>
</html>
"""

if __name__ == '__main__':
    build()
