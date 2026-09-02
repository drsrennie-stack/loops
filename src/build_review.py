#!/usr/bin/env python3
"""Build the answer check sheet.

One file, no folder beside it. Every picture is embedded as a data URI so she
can open it anywhere, mark it up on a plane, and it still works. The flagged
questions come first because those are the ones I actually need her on; the
other thirty five are behind a toggle in case she spots something while she is
in there.

What comes back out is a plain text block she copies and pastes to me. Marking
a question keeps its slide, its number and its current key alongside whatever
she types, so a correction can never arrive detached from the question it
belongs to.
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
FLAGGED_W, PLAIN_W = 1000, 620


def uri(stem, width):
    im = Image.open(os.path.join(PICS, stem + '.jpg')).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)),
                       Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=82, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def build():
    flagged = {q['n'] for q in data.QUESTIONS if q.get('flag')}
    stems_flagged = {q['s'] for q in data.QUESTIONS if q['n'] in flagged}

    pics = {}
    for st in sorted({q['s'] for q in data.QUESTIONS}):
        pics[st] = uri(st, FLAGGED_W if st in stems_flagged else PLAIN_W)

    items = []
    for q in data.QUESTIONS:
        items.append({
            'n': q['n'], 's': q['s'], 'tag': q['tag'], 'a': q['a'],
            'alt': q.get('alt', []), 'flag': q.get('flag', ''),
        })

    payload = json.dumps({'items': items, 'pics': pics},
                         ensure_ascii=False, separators=(',', ':'))

    html = TEMPLATE.replace('/*DATA*/', 'var D = ' + payload + ';')
    path = os.path.join(OUT, 'answer-check-sheet.html')
    open(path, 'w', encoding='utf-8').write(html)
    print('check sheet: %d questions, %d flagged, %.1f MB'
          % (len(items), len(flagged), os.path.getsize(path) / 1e6))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Answer check sheet | Module 1 Practice Lab Exam</title>
<meta name="description" content="Mark the flagged answers right or wrong and send the corrections back.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#1E3D4C; --navy-deep:#142a36; --navy-tint:#EDF1F3;
  --gold:#B8924A; --terra:#8B3A2E;
  --white:#fff; --off:#FAFAF9; --line:#D7DDE0; --muted:#465660;
  --good:#1F5B3A; --good-tint:#E9F2ED;
  --bad:#8B2020; --bad-tint:#F7ECEC;
  --fd:"Plus Jakarta Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --fb:"DM Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --rest:0 1px 3px rgba(0,0,0,.08); --lift:0 8px 16px rgba(0,0,0,.10);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--off);color:var(--navy);font-family:var(--fb);
  font-size:17px;line-height:1.55}
img{max-width:100%;height:auto;display:block}
.skip{position:absolute;left:-9999px;top:0;background:var(--navy);color:#fff;
  padding:12px 18px;z-index:99;border-radius:0 0 8px 0;font-weight:700}
.skip:focus{left:0}
:focus-visible{outline:3px solid var(--navy);outline-offset:3px;border-radius:4px;
  box-shadow:0 0 0 6px rgba(184,146,74,.45)}
.wrap{max-width:1140px;margin:0 auto;padding:26px 20px 80px}
.eyebrow{font-family:var(--fb);font-size:12px;font-weight:700;letter-spacing:.09em;
  text-transform:uppercase;color:var(--terra);margin:0 0 8px}
h1{font-family:var(--fd);font-weight:800;font-size:clamp(1.7rem,3.4vw,2.4rem);
  line-height:1.15;margin:0 0 10px}
h2{font-family:var(--fd);font-weight:600;color:var(--terra);font-size:1.2rem;margin:0 0 10px}
p{margin:0 0 14px;max-width:66ch}
.hint{color:var(--muted);font-size:.92rem}
.card{background:var(--white);border:1px solid var(--line);border-radius:12px;
  padding:22px;box-shadow:var(--rest)}
.btn{font-family:var(--fd);font-weight:700;font-size:1rem;border-radius:9px;
  padding:13px 22px;min-height:48px;cursor:pointer;border:1px solid var(--navy);
  background:var(--navy);color:#fff;transition:background 200ms ease,transform 200ms ease}
.btn:hover{background:var(--navy-deep);transform:translateY(-2px);box-shadow:var(--lift)}
.btn.ghost{background:var(--white);color:var(--navy)}
.btn.ghost:hover{background:var(--navy-tint)}
.btn.sm{font-size:.88rem;padding:10px 16px;min-height:44px}
@media (prefers-reduced-motion: reduce){.btn,.btn:hover{transition:none;transform:none}}
.row{display:flex;flex-wrap:wrap;gap:12px;align-items:center}

/* ---- one question ---- */
.q{background:var(--white);border:1px solid var(--line);border-radius:12px;
  padding:20px;box-shadow:var(--rest);margin:0 0 20px}
.q.done-keep{border-color:var(--good)}
.q.done-change{border-color:var(--terra)}
.qtop{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;margin:0 0 10px}
.qn{font-family:var(--fd);font-weight:800;font-size:1.35rem;color:var(--terra)}
.qtag{font-family:var(--fd);font-weight:700;font-size:1.1rem}
.badge{font-family:var(--fb);font-size:11px;font-weight:700;letter-spacing:.07em;
  text-transform:uppercase;border:1px solid var(--line);border-radius:999px;
  padding:4px 10px;color:var(--muted)}
.badge.f{color:var(--terra);border-color:var(--gold);background:#FBF7EF}
.qgrid{display:grid;gap:20px;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
  align-items:start}
@media (max-width:840px){.qgrid{grid-template-columns:1fr}}
.plate{border:1px solid var(--line);border-radius:8px;padding:8px;background:var(--white)}
.why{background:#FBF7EF;border:1px solid var(--gold);border-radius:9px;
  padding:12px 14px;margin:0 0 14px}
.why p{margin:0;font-size:.95rem}
.keyline{margin:0 0 4px}
.keyline strong{font-family:var(--fd)}
.alts{color:var(--muted);font-size:.9rem;margin:0 0 14px}
fieldset{border:0;padding:0;margin:0 0 12px}
legend{font-family:var(--fd);font-weight:600;font-size:.95rem;padding:0 0 6px}
.choice{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);
  border-radius:9px;padding:11px 15px;min-height:44px;cursor:pointer;margin:0 10px 0 0;
  background:var(--white);font-family:var(--fd);font-weight:600;font-size:.95rem}
.choice input{width:18px;height:18px;accent-color:var(--navy);margin:0}
.choice:hover{background:var(--navy-tint)}
.choice.on-keep{background:var(--good-tint);border-color:var(--good);color:var(--good)}
.choice.on-change{background:var(--bad-tint);border-color:var(--terra);color:var(--terra)}
label.fld{display:block;font-family:var(--fd);font-weight:600;font-size:.9rem;margin:12px 0 5px}
input[type=text],textarea{font-family:var(--fb);font-size:1rem;color:var(--navy);
  background:var(--white);border:1px solid var(--navy);border-radius:9px;
  padding:11px 13px;width:100%;min-height:46px}
textarea{min-height:74px;resize:vertical}
.fix[hidden]{display:none}

/* ---- sticky progress ---- */
.bar{position:sticky;top:0;z-index:20;background:var(--off);
  border-bottom:1px solid var(--line);padding:12px 0;margin:0 0 22px}
.bar .in{display:flex;flex-wrap:wrap;gap:12px;align-items:center;
  max-width:1140px;margin:0 auto;padding:0 20px}
.count{font-family:var(--fd);font-weight:700}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0 0 0 0);white-space:nowrap;border:0}
#outWrap[hidden]{display:none}
#out{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.85rem;
  min-height:230px;white-space:pre}
@media print{.noprint{display:none!important}body{background:#fff}}
</style>
</head>
<body>
<a class="skip" href="#list">Skip to the questions</a>
<div class="bar noprint"><div class="in">
  <span class="count" id="count">0 of 0 marked</span>
  <button class="btn sm ghost" id="toggleAll" type="button" aria-pressed="false">Show all 52</button>
  <button class="btn sm" id="copyBtn" type="button">Copy the corrections</button>
  <span class="hint" id="saved" role="status" aria-live="polite"></span>
</div></div>

<div class="wrap">
<header>
  <p class="eyebrow">BIO 004 &middot; Module 1 Practice Lab Exam</p>
  <h1>Answer check sheet</h1>
</header>

<main>
<div class="card" style="margin:0 0 26px">
  <h2>How this works</h2>
  <p>These are the answers I would not put in front of a class without you looking at them
  first. Each one shows the picture, the answer I keyed, and why I flagged it. Mark it
  <strong>keep</strong> or <strong>change</strong>. If you change it, type what it should
  say. Everything saves in this browser as you go, so you can stop and come back.</p>
  <p>When you are done, press <strong>Copy the corrections</strong> and paste the result back
  to me. Only the ones you touched come out, so a half finished pass is still useful.</p>
  <p class="hint">The pictures are inside this file. It works with no internet and no folder
  beside it.</p>
  <p class="hint" id="allClear" hidden><strong>Nothing is outstanding right now.</strong>
  Every answer has been confirmed, so the whole exam is showing rather than a short list.
  Mark anything you want changed and send it back the same way.</p>
</div>

<div id="list"></div>

<div class="card" id="outWrap" hidden>
  <h2>Paste this back to me</h2>
  <label class="fld" for="out">Your corrections</label>
  <textarea id="out" readonly></textarea>
  <p class="hint" style="margin-top:10px" id="copyNote"></p>
</div>
</main>

<footer style="margin-top:34px;border-top:1px solid var(--line);padding-top:16px">
  <p class="hint">BIO 004 Human Anatomy, Solano Community College. Dr. Sharilyn Rennie</p>
</footer>
</div>

<script>
"use strict";
/*DATA*/

var KEY = "bio004m1check_v1";
var state = read();
/* When nothing is flagged, every answer has been confirmed, so opening on an
   empty list would just look broken. Show the whole exam instead. */
var anyFlag = D.items.some(function(q){ return q.flag; });
var showAll = !anyFlag;

function read(){
  try { var v = JSON.parse(localStorage.getItem(KEY)); return (v && typeof v === "object") ? v : {}; }
  catch(e){ return {}; }
}
function save(){
  try { localStorage.setItem(KEY, JSON.stringify(state)); say("Saved."); }
  catch(e){ say("Could not save in this browser. Copy your corrections before you close the tab."); }
}
var sayTimer = null;
function say(t){
  var el = document.getElementById("saved");
  el.textContent = t;
  clearTimeout(sayTimer);
  sayTimer = setTimeout(function(){ el.textContent = ""; }, 2500);
}
function esc(s){
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;");
}

function render(){
  var host = document.getElementById("list");
  host.innerHTML = "";
  var shown = D.items.filter(function(q){ return showAll || q.flag; });

  shown.forEach(function(q){
    var st = state[q.n] || {};
    var d = document.createElement("section");
    d.className = "q" + (st.mark === "keep" ? " done-keep" : st.mark === "change" ? " done-change" : "");
    d.id = "q" + q.n;

    d.innerHTML =
      '<div class="qtop">'
      + '<span class="qn">' + q.n + '</span>'
      + '<span class="qtag">' + esc(q.tag) + '</span>'
      + (q.flag ? '<span class="badge f">Please check</span>'
                : '<span class="badge">I am confident</span>')
      + '</div>'
      + '<div class="qgrid">'
      + '<div class="plate"><img src="' + D.pics[q.s] + '" alt="Slide for question '
      + q.n + '. Identify it by eye."></div>'
      + '<div class="pane"></div>'
      + '</div>';

    var pane = d.querySelector(".pane");

    if (q.flag){
      var why = document.createElement("div");
      why.className = "why";
      why.innerHTML = "<p><strong>Why I flagged it.</strong> " + esc(q.flag) + "</p>";
      pane.appendChild(why);
    }

    var kl = document.createElement("p");
    kl.className = "keyline";
    kl.innerHTML = "I keyed it: <strong>" + esc(q.a) + "</strong>";
    pane.appendChild(kl);

    if (q.alt && q.alt.length){
      var al = document.createElement("p");
      al.className = "alts";
      al.textContent = "Also accepted: " + q.alt.join(", ");
      pane.appendChild(al);
    }

    var fs = document.createElement("fieldset");
    fs.innerHTML = '<legend>Is this right?</legend>';
    [["keep", "Keep it"], ["change", "Change it"]].forEach(function(o){
      var lab = document.createElement("label");
      lab.className = "choice" + (st.mark === o[0] ? " on-" + o[0] : "");
      lab.innerHTML = '<input type="radio" name="m' + q.n + '" value="' + o[0] + '"'
        + (st.mark === o[0] ? " checked" : "") + '><span>' + o[1] + '</span>';
      lab.querySelector("input").addEventListener("change", function(){
        setMark(q.n, o[0]);
      });
      fs.appendChild(lab);
    });
    pane.appendChild(fs);

    var fix = document.createElement("div");
    fix.className = "fix";
    fix.hidden = st.mark !== "change";
    fix.innerHTML =
      '<label class="fld" for="a' + q.n + '">What it should say</label>'
      + '<input type="text" id="a' + q.n + '" value="' + esc(st.a || "") + '">'
      + '<label class="fld" for="alt' + q.n + '">Anything else to accept, separated by commas</label>'
      + '<input type="text" id="alt' + q.n + '" value="' + esc(st.alt || "") + '">'
      + '<label class="fld" for="t' + q.n + '">Change the question itself, if it needs it</label>'
      + '<input type="text" id="t' + q.n + '" value="' + esc(st.tag || "") + '" placeholder="'
      + esc(q.tag) + '">'
      + '<label class="fld" for="n' + q.n + '">Note for me</label>'
      + '<textarea id="n' + q.n + '">' + esc(st.note || "") + '</textarea>';
    pane.appendChild(fix);

    ["a", "alt", "t", "n"].forEach(function(k){
      var el = fix.querySelector("#" + k + q.n);
      el.addEventListener("input", function(){
        var s = state[q.n] || (state[q.n] = {});
        s[{a: "a", alt: "alt", t: "tag", n: "note"}[k]] = el.value;
        save(); tally();
      });
    });

    host.appendChild(d);
  });
  tally();
}

function setMark(n, mark){
  var s = state[n] || (state[n] = {});
  s.mark = mark;
  save();
  var card = document.getElementById("q" + n);
  card.className = "q done-" + mark;
  card.querySelector(".fix").hidden = (mark !== "change");
  Array.prototype.forEach.call(card.querySelectorAll(".choice"), function(l){
    var v = l.querySelector("input").value;
    l.className = "choice" + (v === mark ? " on-" + v : "");
  });
  tally();
}

function tally(){
  var flagged = D.items.filter(function(q){ return q.flag; });
  var pool = flagged.length ? flagged : D.items;
  var done = pool.filter(function(q){ return state[q.n] && state[q.n].mark; }).length;
  document.getElementById("count").textContent = flagged.length
    ? done + " of " + flagged.length + " flagged questions marked"
    : "Nothing outstanding. " + done + " of " + pool.length + " marked.";
}

document.getElementById("toggleAll").addEventListener("click", function(){
  showAll = !showAll;
  this.setAttribute("aria-pressed", String(showAll));
  this.textContent = showAll ? "Show only the ones I flagged"
                             : "Show all " + D.items.length;
  render();
});

document.getElementById("copyBtn").addEventListener("click", function(){
  var lines = ["Module 1 practice exam, answer corrections", ""];
  var touched = 0;
  D.items.forEach(function(q){
    var s = state[q.n];
    if (!s || !s.mark) return;
    touched++;
    if (s.mark === "keep"){
      lines.push("Q" + q.n + "  KEEP  (" + q.a + ")");
    } else {
      lines.push("Q" + q.n + "  CHANGE");
      lines.push("   was:    " + q.a);
      lines.push("   should be: " + (s.a || "[not filled in]"));
      if (s.alt) lines.push("   also accept: " + s.alt);
      if (s.tag) lines.push("   new question: " + s.tag);
      if (s.note) lines.push("   note: " + s.note.replace(/\n/g, " "));
    }
  });
  if (!touched){
    lines = ["Nothing marked yet."];
  }
  var text = lines.join("\n");
  var wrap = document.getElementById("outWrap");
  var out = document.getElementById("out");
  wrap.hidden = false;
  out.value = text;
  out.focus();
  out.select();
  var note = document.getElementById("copyNote");
  function ok(){ note.textContent = "Copied. Paste it into the chat."; }
  function manual(){ note.textContent = "Select all of the box above and copy it by hand."; }
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(ok, manual);
  } else {
    try { document.execCommand("copy") ? ok() : manual(); } catch(e){ manual(); }
  }
});

if (!anyFlag){
  var ac = document.getElementById("allClear");
  if (ac) ac.hidden = false;
  var tb = document.getElementById("toggleAll");
  if (tb){ tb.hidden = true; }
}
render();
</script>
</body>
</html>
"""

if __name__ == '__main__':
    build()
