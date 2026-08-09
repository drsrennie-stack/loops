# Topic notes on every video page, plus the Loops index

Repo root, overwriting. Nothing deleted.

## 1. The notes buttons were wrong. All 38 video pages fixed.

"Download the notes" pointed at, depending on the page:

- `#` — a dead link, on **12** pages
- `BIO004-Week1-Notes.pdf#page=11` — the old summer week-1 PDF, on 4 pages
- `Heart.pptx` — a PowerPoint, not notes
- nothing at all, on 19 pages that had no notes link

**Not one page pointed at your topic HTML notes.**

Every video page now carries a button per matching topic notes page:
**51 note buttons across 38 pages**, all HTML, all opening `_top`. The 12 dead
`#` anchors are gone.

Example, `blood-vessels-concept-videos.html`:

```
Notes: Blood Vessels
Notes: Vessel Disorders and Fetal Circulation
Notes: Upper Limb Vessels and Nerves
```

All 41 of your `m1` to `m5` notes pages are reachable this way.

## 2. `loops-index.js` — NEW

The 39 Loops, read from the `LOOPS` array in `drsrennie-stack/loops`, each
tagged with the competencies it gives evidence for. Ids, titles and units come
from your file, not invented. 2,005 frames, and I verified the first frame of
all 39 resolves on disk.

**The important part:** ten competencies had **no card coverage at all** —
upper extremity lab muscles, nerves and vessels, lower limb vessels and
nerves, and the head and neck lab muscles. Cadaver work that multiple choice
cannot assess. **Every one is covered by a Loop.**

Cards alone: 186 of 196. Loops alone: 164 of 196.
**Cards plus Loops: 196 of 196.** Neither gets there without the other.

## 3. `mastery-evidence.js` — NEW

One append-only store, `bio004-evidence-v1`, that every source writes the same
shape into: `{comp, source, got, of, at}` where source is `card`, `loop` or
`draw`.

Recall Rx is not asked to change. This reads its store directly and folds card
history in, so cards keep counting either way.

`summary()` keeps the three sources **separate** rather than averaging them.
That is deliberate: a student can recognise every structure on a card and
still be unable to draw it from a blank page. "Strong on cards, weak on
drawing" is the signal worth acting on, and averaging destroys it.

`weakest()` also ranks never-attempted below tried-and-failed, and flags
anything under three attempts as thin rather than reporting a percentage from
one data point.

This is the foundation the drawing assignments and the rebuilt weak spot
board plug into. Neither is built yet.
