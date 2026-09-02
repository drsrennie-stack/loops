/* ============================================================
   BIO 004 Human Anatomy, Fall 2026
   mastery-evidence.js

   ONE EVIDENCE STORE, THREE ENGINES.

   THE PROBLEM
   -----------
   Three separate engines each kept score in its own place, in its
   own shape, and nothing read across them:

     Recall Rx      localStorage['bio004-recall-v2']
                    topics[topicId].cards[cardId].history[]
     Loops          localStorage['loopScores_v1']
                    { loopId: [ {t, right, denom, pct, ms} ] }
     Drawing        nothing. mastery-canvas.html had no storage
                    call of any kind.
     Mastery OS     localStorage['bio004-progress'], a key nothing
                    ever wrote to.

   So the weak spot board could only ever see cards. A student who
   had run every Loop for a unit still read as no evidence.

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

   NEITHER ENGINE IS ASKED TO CHANGE
   ---------------------------------
   Recall Rx and Loops both keep writing exactly what they already
   wrote. This file reads their stores where they sit and translates
   both into competencies. Adding a fourth engine later means adding
   one more reader here, nothing else.

   The source field is kept on every entry because the Mastery OS
   needs to know which engine to send a student back to when it
   names a weak spot. It is not there to build a side by side
   comparison of the engines.
   ============================================================ */

(function () {
  'use strict';

  var KEY = 'bio004-evidence-v1';
  var RECALL_KEY = 'bio004-recall-v2';
  var LOOPS_KEY = 'loopScores_v1';        /* old, nothing writes it */
  var STATION_KEY = 'loopsEngine_v1';     /* what the Loops app really writes */

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
  /* conf is the student's confidence BEFORE they attempted it:
     'high' | 'med' | 'low'. Recorded separately from the score so the
     two can be compared. High confidence with low retrieval is the
     most useful signal in the whole system: it is the gap a student
     cannot feel, and it is exactly what they will walk into an exam
     believing they know. */
  function record(comps, source, got, of, conf, when) {
    if (!comps) return false;
    if (typeof comps === 'string') comps = [comps];
    if (!of || of < 0) return false;
    var at = when || new Date().toISOString();
    var list = read();
    comps.forEach(function (c) {
      list.push({ comp: c, source: source, got: got, of: of, conf: conf || null, at: at });
    });
    /* Keep the log bounded. 4000 entries is far more than a term
       produces, and trimming the oldest keeps recent work honest. */
    if (list.length > 4000) list = list.slice(list.length - 4000);
    return write(list);
  }

  /* Fold Recall Rx's own store in, without asking it to change.
     Its truth is history[], one entry per attempt, under
     topics[topicId].cards[cardId], shaped
     { at: ISO, rating: n, correct: bool }.
     card-competency-map.js says which competencies a topic speaks to.

     ONE ENTRY PER ATTEMPT, NOT ONE PER TOPIC.
     An earlier version rolled a whole topic up into a single entry
     stamped with the most recent attempt's time. Term totals came out
     right, but anything that asks "what happened today" came out very
     wrong: a student who answered eight cards this morning on a topic
     they have drilled since August would have been told they attempted
     two hundred items today, and the time estimate had one timestamp to
     work from instead of eight. Attempts carry their own times, so they
     are kept apart. */
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
      Object.keys(cards).forEach(function (cid) {
        var r = cards[cid] || {};
        var hist = r.history;
        if (hist && hist.length) {
          hist.forEach(function (h) {
            if (!h) return;
            var w = h.at || h.date || h.reviewedAt || '';
            entry.comps.forEach(function (c) {
              out.push({ comp: c, source: 'card', got: h.correct ? 1 : 0, of: 1, conf: null, at: w });
            });
          });
        } else if (r.attempts) {
          /* Older stores kept a running count with no per-attempt time.
             Nothing better to date it with, so it is left undated and
             counts toward the term but never toward a single day. */
          entry.comps.forEach(function (c) {
            out.push({ comp: c, source: 'card', got: r.correct || 0, of: r.attempts, conf: null, at: '' });
          });
        }
      });
    });
    return out;
  }

  /* Fold the Loops engine in, without asking it to change either.

     THE ONE FACT THAT MAKES THIS WORK
     ---------------------------------
     Loops and this course site are BOTH served from
     drsrennie-stack.github.io. localStorage is scoped to an origin,
     not to a path, so the Loops app's own history is readable from
     here directly. No postMessage bridge, no export button, no
     change to the Loops code.

     FIXED 2 SEPTEMBER 2026. THIS READ THE WRONG KEY.
     ------------------------------------------------
     It read loopScores_v1. The Loops app has never written that key;
     it is from a build that was replaced. What Loops actually writes
     is loopsEngine_v1, ONE RECORD PER STATION, keyed "<loopId>#<index>":

       { seen, again, hard, good, easy, recent:[], spell, lastConf, over }

     So fromLoops() found nothing, returned [], and every competency
     whose only evidence was Loops read as untouched no matter how
     much loop work a student had done. mastery-os-fall-2026.html had
     already been fixed to read the station store directly; this file
     had not, so every OTHER page that asks BIO004_EVIDENCE for a
     rollup (brain dump, day review, practice lecture exam, the
     drawing canvas) was still blind to Loops.

     Both keys are read now. The station store is the real one; the
     old key stays supported in case anything ever writes it.

     Scoring: good and easy count as right, hard as half right,
     again and unopened as wrong. That is the same weighting the
     Loops app uses for its own weakness score, so the two never
     disagree. Watch-only stations record nothing and contribute
     nothing, which is correct: watching is not retrieval. */
  function fromLoops() {
    var LOOPS = window.BIO004_LOOPS;
    if (!LOOPS) return [];
    var byId = {};
    LOOPS.forEach(function (l) { byId[l.id] = l.comps || []; });
    var out = [];

    /* the real store: one record per station */
    var st;
    try { st = JSON.parse(localStorage.getItem(STATION_KEY) || 'null'); }
    catch (e) { st = null; }
    if (st) {
      var agg = {};
      Object.keys(st).forEach(function (k) {
        var cut = k.lastIndexOf('#');
        if (cut < 1) return;
        var loopId = k.slice(0, cut);
        if (!byId[loopId] || !byId[loopId].length) return;
        var r = st[k] || {};
        if (!r.seen) return;
        var a = agg[loopId] || (agg[loopId] = { got: 0, of: 0, at: '' });
        a.got += (r.good || 0) + (r.easy || 0) + 0.5 * (r.hard || 0);
        a.of  += r.seen;
        var when = r.last || r.at || null;
        if (when) {
          var iso = '';
          try { iso = new Date(when).toISOString(); } catch (e) { iso = ''; }
          if (iso > a.at) a.at = iso;
        }
      });
      Object.keys(agg).forEach(function (loopId) {
        var a = agg[loopId];
        if (!a.of) return;
        byId[loopId].forEach(function (c) {
          out.push({ comp: c, source: 'loop',
                     got: Math.round(a.got * 100) / 100, of: a.of,
                     conf: null, at: a.at });
        });
      });
    }

    /* the old per-session store, still honoured if anything writes it */
    var legacy;
    try { legacy = JSON.parse(localStorage.getItem(LOOPS_KEY) || 'null'); }
    catch (e) { legacy = null; }
    if (legacy) {
      Object.keys(legacy).forEach(function (loopId) {
        var comps = byId[loopId];
        if (!comps || !comps.length) return;
        var runs = legacy[loopId];
        if (!runs || !runs.length) return;
        runs.forEach(function (r) {
          if (!r || !r.denom) return;
          var at = '';
          try { at = new Date(r.t).toISOString(); } catch (e) { at = ''; }
          comps.forEach(function (c) {
            out.push({ comp: c, source: 'loop', got: r.right || 0, of: r.denom, conf: null, at: at });
          });
        });
      });
    }
    return out;
  }

  /* Which loops a student has actually run, for "you have not opened
     this one yet" messaging on the board. */
  function loopsTouched() {
    /* which loops have been opened at all. Reads the station store and
       rolls "<loopId>#<index>" keys up to loop ids. */
    var out = {};
    var st;
    try { st = JSON.parse(localStorage.getItem(STATION_KEY) || 'null'); }
    catch (e) { st = null; }
    if (st) Object.keys(st).forEach(function (k) {
      var cut = k.lastIndexOf('#');
      if (cut < 1) return;
      var r = st[k];
      if (r && r.seen) (out[k.slice(0, cut)] = out[k.slice(0, cut)] || []).push(r);
    });
    var legacy;
    try { legacy = JSON.parse(localStorage.getItem(LOOPS_KEY) || 'null'); }
    catch (e) { legacy = null; }
    if (legacy) Object.keys(legacy).forEach(function (id) { if (!out[id]) out[id] = legacy[id]; });
    return out;
  }

  /* Everything, cards and Loops included, as one list. */
  function all() {
    return fromCards().concat(fromLoops()).concat(read());
  }

  /* Per-competency rollup, split by source so the board can show
     where the weakness actually is rather than one blended number. */
  function summary() {
    var out = {};
    all().forEach(function (e) {
      var s = out[e.comp] || (out[e.comp] = {
        card: { got: 0, of: 0 }, loop: { got: 0, of: 0 }, draw: { got: 0, of: 0 },
        got: 0, of: 0, last: '', lastConf: null
      });
      var bucket = s[e.source];
      if (bucket) { bucket.got += e.got; bucket.of += e.of; }
      s.got += e.got; s.of += e.of;
      if (e.at && e.at > s.last) { s.last = e.at; if (e.conf) s.lastConf = e.conf; }
    });
    Object.keys(out).forEach(function (id) {
      var s = out[id];
      s.pct = s.of ? Math.round(s.got / s.of * 100) : null;
      /* Overconfident: they said high or medium going in, and scored
         under 60. Worth surfacing above a plain low score, because the
         student does not know this one is a problem. */
      s.overconfident = (s.pct !== null && s.pct < 60 &&
                         (s.lastConf === 'high' || s.lastConf === 'med'));
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
    fromLoops: fromLoops,
    loopsTouched: loopsTouched,
    all: all,
    summary: summary,
    weakest: weakest,
    loopsFor: loopsFor,
    clear: clear,
    KEY: KEY
  };
})();
