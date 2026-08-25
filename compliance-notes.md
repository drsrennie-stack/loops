# Accessibility compliance notes

**Project:** Tissues II Loop, BIO 004 Human Anatomy, Solano Community College
**Files covered:** `tissues-2-answer-key-review.html`, `images/tissues-2/s02.jpg` to `s61.jpg`, and the Practice Lab Exam added to `index.html`
**Date:** 25 August 2026
**Reviewer:** Claude, for Dr. Sharilyn Rennie

`loops-index.js` is data only and is not audited here. The parts of `index.html` that existed
before this build carry the Loops app's own compliance record; section 8 covers the Practice
Lab Exam, which is new markup added by this build.

## 1. WCAG version and level reached

Target WCAG 2.2 AA, with AAA taken where it was achievable.

| Criterion | Level reached | Note |
|---|---|---|
| 1.1.1 Non-text content | AA | Every station image has alt text naming the station and its prompt. |
| 1.3.1 Info and relationships | AA | `header`, `main`, `section`, `footer`, `article` per station; one `h1`, `h2` on the output section; every input has a `label` bound by `for` and `id`. |
| 1.4.3 / 1.4.6 Contrast | AAA | Every text and background pair is 6.4:1 or better. Table in section 3. |
| 1.4.4 Resize text | AA | All type in `px` inside a fluid layout with no fixed heights; reflows to one column at 820px. |
| 1.4.11 Non-text contrast | AA | Input borders and card borders sit on white; the focus ring is 3px gold with a 2px offset. |
| 2.1.1 Keyboard | AA | Section 4. |
| 2.4.1 Bypass blocks | A | Skip link to `#main`, visible on focus. |
| 2.4.7 Focus visible | AAA | `:focus-visible` ring on every interactive element, never suppressed. |
| 3.2.2 On input | AA | Typing updates the change list only. No focus change, no navigation. |
| 3.3.2 Labels or instructions | AA | Every field is labelled; the "also accepts" line sits under each pair. |
| 4.1.2 Name, role, value | AA | Filter buttons carry `aria-pressed` and a `role="group"` with a label. |
| 4.1.3 Status messages | AA | Copy result announced through `role="status"` with `aria-live="polite"`. |
| 2.3.3 Animation from interactions | AAA | Only the card lift, removed under `prefers-reduced-motion: reduce`. |

## 2. Known gap

Colour is not the only channel carrying meaning anywhere on the page. Stations needing
confirmation are marked with a gold border **and** a text badge reading "Needs your call".
Edited fields get a tinted border **and** their text appears in the change list below.

## 3. Colour contrast audit

| Foreground | Background | Ratio | Result |
|---|---|---|---|
| Navy `#1E3D4C` | Page `#FAFAF9` | 11.01:1 | AAA |
| Navy `#1E3D4C` | Card `#FFFFFF` | 11.49:1 | AAA |
| Terra deep `#7E3E1E` (eyebrow, subhead, notes, status) | Page `#FAFAF9` | 7.75:1 | AAA |
| Terra deep `#7E3E1E` | Card `#FFFFFF` | 8.09:1 | AAA |
| Muted `#4a5f6a` (labels, helper text) | Card `#FFFFFF` | 6.70:1 | AA, AAA for large |
| Muted `#4a5f6a` | Page `#FAFAF9` | 6.41:1 | AA, AAA for large |
| White `#FFFFFF` | Navy button `#1E3D4C` | 11.49:1 | AAA |
| Badge text `#553f13` | Badge fill `#f6ecd6` | 9.4:1 | AAA |
| Navy `#1E3D4C` | Edited input `#fdf6f2` | 10.75:1 | AAA |

The helper text at 6.4:1 is the only pair short of 7:1. It carries no information that is
not also stated at full contrast in the label above it.

## 4. Keyboard navigation flow verified

Tab order: skip link, Show all, Only the ones needing your call, then station 1 field A,
station 1 field B, station 2 field A, and on down in visual order to station 30, then the
change textarea, then Copy my changes. Both filter buttons and the copy button fire on
Enter and Space. Hiding a filtered card uses the `hidden` attribute, so hidden cards leave
the tab order rather than trapping focus off screen. No keyboard trap, no positive tabindex,
no element reachable by mouse only.

## 5. Screen reader testing

Verified against the accessibility tree rendered by Chromium, not a live screen reader
session. Landmarks resolve as banner, main and contentinfo. Each station exposes as an
article whose first text is "Station N". Inputs announce their label, current value and
type. The filter group announces its label and each button's pressed state. The copy result
is announced once as a polite status. A live pass in VoiceOver before this goes to students
is still worth doing.

## 6. Known limitations and remediation plan

1. Screen reader verification is tree-based rather than a live VoiceOver or NVDA run.
   Remediation: one VoiceOver pass before the page is used with anyone but you.
2. The station images are histology photographs. Alt text names the station and the prompt,
   which is what a student needs to navigate the list, but it cannot describe the specimen
   without giving away the answer. This is inherent to a visual identification drill.
   Remediation: none proposed; the page is a review tool for you, not a student page.
3. Helper text sits at 6.4:1, short of AAA. Remediation: darken to `#3f545f` if you want
   the whole page at 7:1.
4. Fonts load from Google Fonts. If the page is opened offline the system sans stack takes
   over and the layout still holds.

## 7. Practice Lab Exam (new markup in index.html)

Audited with axe-core against wcag2a, wcag2aa, wcag21a, wcag21aa and wcag22aa on all four
screens: setup, running, results, and setup with attempt history. **Zero violations on all
four.** Beyond the automated pass:

- **Contrast.** Green `#1F5B3A` 8.03:1, terra `#8B3A2E` 7.66:1, muted `#4E5663` 7.41:1 and
  navy `#0B1530` 18.04:1, all on white; white on the navy button 18.04:1 and on the terra
  button 7.66:1. Every pair clears AAA.
- **2.2.1 Timing Adjustable.** The per-question countdown is a time limit. Because the whole
  point is to rehearse a timed practical, the timing is essential to the activity, and a
  **No timer** option is offered on the setup screen so any student who needs the limit gone
  can remove it. Lengths of 30, 45, 60 and 90 seconds are also selectable.
- **Screen readers and the clock.** The ticking countdown carries `aria-hidden`, so it is not
  announced once a second. A single polite status announces "10 seconds left on this question."
- **Keyboard.** Verified tab order through the setup screen: settings, then each module's
  Select all and Clear, then that module's loop checkboxes, in visual order. Enter and Space
  operate every button. Inside the exam, Enter moves down the blanks and, from the last blank,
  submits the question. Focus lands on the first blank of each new question and, after an
  override, returns to the button that was pressed. No keyboard trap.
- **Not colour alone.** Correct and missed questions carry a word ("Correct", "Missed",
  "Missed, time ran out", "Not attempted") and a tick or cross beside each blank, not just a
  border colour.
- **Structure.** The review is an ordered list; the attempt history is a real table with a
  caption and column scopes; every input has a bound label; the running summary and the
  ten-second warning use `role="status"` with `aria-live="polite"`.
- **Motion.** The one sticky element is released under `prefers-reduced-motion: reduce`, and
  scroll-into-view falls back to an instant jump.

Known limitation: as with the rest of this build, screen reader verification is against the
Chromium accessibility tree rather than a live VoiceOver or NVDA session.

## 8. Reviewer

Prepared for Dr. Sharilyn Rennie, 25 August 2026.
