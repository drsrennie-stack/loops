/* ============================================================
   BIO 004 Human Anatomy, Fall 2026
   mastery-evidence.js

   ONE EVIDENCE STORE, THREE SOURCES.

   THE PROBLEM
   -----------
   Every study tool in this course kept its own score in its own
   place, in its own shape:

     Recall Rx      localStorage['bio004-recall-v2']
                    topics[topicId].cards[cardId].history[]
     Loops          nothing. Not recorded anywhere.
     Drawing        nothing. mastery-canvas.html has no storage
                    call of any kind.
     Mastery OS     localStorage['bio004-progress'], a key nothing
                    ever wrote to.

   So the weak spot board could only ever see cards, and a
   competency a student had drawn ten times or watched every Loop
   for still read as no evidence.

   WHAT THIS IS
   ------------
   A single append-only log, keyed by competency, that every
   source writes the same shape into:

     { comp, source, got, of, at }

       comp    competency id from competenciesfall2026.js
       source  'card' | 'loop' | 'draw'
       got     how many they got right
       of      how many were possible
       at      ISO timestamp

   Recall Rx is NOT asked to change. mastery-evidence.js reads its
   store directly and folds it in, so card history keeps working
   whether or not a student ever opens anything else.

   WHY SOURCE MATTERS
   ------------------
   Recall and reconstruction fail differently. A student can
   recognise every structure on a multiple-choice card and be
   unable to draw the thing from a blank page. Keeping the source
   on every entry is what lets the board say "strong on cards,
   weak on drawing", which is the signal worth acting on. Averaging
   them into one number throws that away.
   ============================================================ */

(function () {
  'use strict';

  var KEY = 'bio004-evidence-v1';
  var RECALL_KEY = 'bio004-recall-v2';

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return [];
      var v = JSON.parse(raw);
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }
  }

  function write(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); return true; }
    catch (e) { return false; }
  }

  /* Record one piece of evidence. comps may be a single id or a
     list, because one drawing or one Loop usually speaks to
     several competencies at once. */
  function record(comps, source, got, of, when) {
    if (!comps) return false;
    if (typeof comps === 'string') comps = [comps];
    if (!of || of < 0) return false;
    var at = when || new Date().toISOString();
    var list = read();
    comps.forEach(function (c) {
      list.push({ comp: c, source: source, got: got, of: of, at: at });
    });
    /* Keep the log bounded. 4000 entries is far more than a term
       produces, and trimming the oldest keeps recent work honest. */
    if (list.length > 4000) list = list.slice(list.length - 4000);
    return write(list);
  }

  /* Fold Recall Rx's own store in, without asking it to change.
     Its truth is history[], one entry per attempt, under
     topics[topicId].cards[cardId]. card-competency-map.js says
     which competencies a topic speaks to. */
  function fromCards() {
    var MAP = window.BIO004_CARD_COMPETENCY_MAP;
    if (!MAP) return [];
    var st;
    try { st = JSON.parse(localStorage.getItem(RECALL_KEY) || 'null'); }
    catch (e) { return []; }
    if (!st || !st.topics) return [];

    var out = [];
    Object.keys(st.topics).forEach(function (tid) {
      var entry = MAP[tid];
      if (!entry || !entry.comps.length) return;
      var cards = (st.topics[tid] && st.topics[tid].cards) || {};
      var got = 0, of = 0, at = '';
      Object.keys(cards).forEach(function (cid) {
        var r = cards[cid] || {};
        var hist = r.history;
        if (hist && hist.length) {
          hist.forEach(function (h) {
            of += 1;
            if (h && h.correct) got += 1;
            var w = h && (h.at || h.date || h.reviewedAt);
            if (w && w > at) at = w;
          });
        } else if (r.attempts) {
          of += r.attempts; got += (r.correct || 0);
        }
      });
      if (!of) return;
      entry.comps.forEach(function (c) {
        out.push({ comp: c, source: 'card', got: got, of: of, at: at });
      });
    });
    return out;
  }

  /* Everything, cards included, as one list. */
  function all() {
    return fromCards().concat(read());
  }

  /* Per-competency rollup, split by source so the board can show
     where the weakness actually is rather than one blended number. */
  function summary() {
    var out = {};
    all().forEach(function (e) {
      var s = out[e.comp] || (out[e.comp] = {
        card: { got: 0, of: 0 }, loop: { got: 0, of: 0 }, draw: { got: 0, of: 0 },
        got: 0, of: 0, last: ''
      });
      var bucket = s[e.source];
      if (bucket) { bucket.got += e.got; bucket.of += e.of; }
      s.got += e.got; s.of += e.of;
      if (e.at && e.at > s.last) s.last = e.at;
    });
    Object.keys(out).forEach(function (id) {
      var s = out[id];
      s.pct = s.of ? Math.round(s.got / s.of * 100) : null;
      ['card', 'loop', 'draw'].forEach(function (k) {
        s[k].pct = s[k].of ? Math.round(s[k].got / s[k].of * 100) : null;
      });
      /* Under three attempts a percentage is noise, not a signal.
         The board should say "needs data", not "50%". */
      s.thin = s.of < 3;
    });
    return out;
  }

  /* Weakest first. Competencies with no evidence at all come last,
     not first, because "never tried" and "tried and failed" are
     different problems and only one of them is a weak spot. */
  function weakest(limit) {
    var sum = summary();
    var comps = window.BIO004_COMPETENCIES || [];
    var rows = comps.map(function (c) {
      var s = sum[c.id];
      return {
        id: c.id, name: c.name, system: c.system, general: c.general,
        week: c.week, yield: c.yield,
        pct: s ? s.pct : null,
        of: s ? s.of : 0,
        thin: s ? s.thin : true,
        bySource: s ? { card: s.card, loop: s.loop, draw: s.draw } : null,
        untouched: !s
      };
    });
    rows.sort(function (a, b) {
      if (a.untouched !== b.untouched) return a.untouched ? 1 : -1;
      if (a.thin !== b.thin) return a.thin ? 1 : -1;
      return (a.pct === null ? 101 : a.pct) - (b.pct === null ? 101 : b.pct);
    });
    return limit ? rows.slice(0, limit) : rows;
  }

  /* Loops that would help with a competency, for "fix this weak
     spot" buttons on the board. */
  function loopsFor(compId) {
    return (window.BIO004_LOOPS || []).filter(function (l) {
      return l.comps.indexOf(compId) >= 0;
    });
  }

  function clear() { try { localStorage.removeItem(KEY); } catch (e) {} }

  window.BIO004_EVIDENCE = {
    record: record,
    all: all,
    summary: summary,
    weakest: weakest,
    loopsFor: loopsFor,
    clear: clear,
    KEY: KEY
  };
})();
