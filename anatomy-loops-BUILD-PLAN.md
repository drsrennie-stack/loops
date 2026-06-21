# Anatomy Loops, Build Plan

A short plan for the next round of work on the Anatomy Loops practice app. Nothing here is built yet. This captures what we agreed is possible and the order to build it. Last updated June 21, 2026.

## Where things stand today

Five loops live in the app: Intro, Tissues, Skin, Bone, and Axial Skull. Skull is the first dark-themed loop. The app runs from static files on GitHub Pages, all student data (scores, history, and anything new below) lives in the student's own browser, and no names or identifiers are ever stored. That static, device-local, name-free setup is the posture we keep.

The one true limit: anything the whole class shares has to live in the repo, and the page cannot write back to the repo. So a shared, class-wide upload bank is the only item on our wish list that would need a real backend. Everything else fits the current setup.

## What we're building

### 1. Session length (student picks how many)

A control next to the existing ones: All, 10, 20, 50, 100. The app builds a queue of exactly that many, draws randomly, reshuffles without immediate repeats if the number is larger than the category, then stops and shows the score. This is the biggest single win, because everyone is scored out of the same number, which makes scores mean something.

### 2. Multiple topic selection

Checkboxes for each topic on the front page. A student ticks the topics their exam covers, the app pools the cards from just those folders, shuffles them together, and runs one scored session. The results screen breaks the score down by topic (for example Skull 85 percent, Bone 60 percent) so they see exactly where to keep studying. Picking topics is just picking which folders feed the pool, so the format makes this easy.

### 3. One consistent frame and typing box

Replace the per-loop dark theme with a single steady frame around every loop. The black on the skull pages comes from the images themselves, not from a theme that flips partway through a mixed review. The typing box and controls look the same everywhere, white box below the image, consistent across black and white slides. This matters specifically because a multi-topic review mixes black skull images with white histology images in one run.

Open decision: keep the yellow accent on the typing box, or go neutral.

### 4. Self-rating: Again, Hard, Good, Easy

Replace the three self-check buttons (Correct, Misspelled, Incorrect) with four: Again, Hard, Good, Easy. The student types, reveals, then taps one.

- Again: did not know it or missed it. Strongest weakness signal.
- Hard: knew it but struggled, or got it but misspelled.
- Good: recalled it correctly.
- Easy: knew it instantly.

These four absorb the old three (misspelled folds into Hard) while recording how well each card was recalled. Important: these ratings feed the weakness dashboard only. They do not schedule anything. No due dates, no daily queue, no "you have cards due today." The student always drives.

Open decision: fold misspelled into Hard, or keep spelling as its own visible outcome on top of the four.

### 5. Weakness dashboard (and optional drill)

Each card keeps a small running tally of its ratings in the browser. The dashboard reads those tallies and shows where the student is weak, by topic and by individual structure, weighted toward what they keep missing recently. Weakness is only ever an option: a "Drill my weak ones" button they can choose to press, optionally narrowed to selected topics, never an order.

Open decision: the exact definition of weak (for example, recent Again and Hard frequency, or a rolling ease score that drops with Again and rises with Easy).

### 6. Onboarding

Two pieces, kept light:

- A one-time intro the first time a student opens the app, Mac-setup style. A few dismissible cards explaining the modes. Shown once, never nags again.
- A short per-session builder, two or three steps (pick topics, pick how many, go) that remembers the last choices. Returning students land on a one-tap "start again, same as last time" and only open the full picker to change something. Always skippable.

Built keyboard-accessible from the start, to hold the WCAG 2.2 AA floor.

Decided: include the one-time intro (both pieces). Open: whether the intro leans toward how to study well or how the buttons work.

### 7. Authoring tool (for you)

A separate local page, not the student app, where you drag in a PDF or images, it auto-renders and resizes them, you type the answer key and pick the category, and it hands back a ready images folder plus the exact data to drop in, or a fully rebuilt index.html. You still do one commit to publish, but the manual work I do by hand now becomes drag, type, download.

### 8. Personal student-made cards

A student can upload an image, type the key, choose a category, and have it become a real card in their own practice, scored like the rest. It stays on their device, private and name-free. They can export their personal deck as a single file (images travel inside it) to move it to another device or hand it to you. A shared class bank is out of scope here, that is the backend project.

## Suggested order

1. Session length. Quick and immediately useful.
2. Multiple topic selection with per-topic score breakdown.
3. Consistent frame and typing box.
4. Self-rating buttons and the item-level memory behind them.
5. Weakness dashboard and the optional weak-ones drill.
6. Onboarding intro and per-session builder.
7. Authoring tool.
8. Personal student-made cards.

We can reorder freely, or start with whichever you most want to see working.

## Decisions to settle before or during the build

- Yellow accent or neutral on the consistent typing box.
- Misspelled folded into Hard, or kept as its own outcome.
- The definition of weak.
- The intro's tone (how to study well, or how the buttons work). One-time intro is confirmed in.
- Confirm everything stays device-local for now (no logins, no backend).
