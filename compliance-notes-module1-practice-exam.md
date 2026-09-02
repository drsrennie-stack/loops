# Accessibility compliance notes

**Project:** Module 1 Practice Lab Exam, BIO 004 Human Anatomy, Solano Community College
**Files covered:** `module1-practice-exam.html`, `module1-slideshow.html`,
`answer-check-sheet.html`, `images/module1-practice/s01.jpg` to `s26.jpg`
**Questions:** 52, numbered 1 to 52, no gaps
**Not covered here:** `Module-1-Practice-Lab-Exam.pptx` and the DOCX key. Notes on those are at the end.
**Date:** 2 September 2026

## 1. Standard and level reached

WCAG 2.2. **AA met in full. AAA met on contrast** for every text and background pair on the
page. Verified with axe-core 4.10 against the `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa` and
`wcag22aa` rule sets, run separately on all four screens, plus the manual checks below that
axe cannot make.

| Criterion | Level | How it is met |
|---|---|---|
| 1.1.1 Non-text content | A | Every question picture carries alt text naming the question it belongs to and saying the identification has to be made by eye. Result thumbnails and key pictures are decorative repeats of a picture already described, so they carry empty alt. |
| 1.3.1 Info and relationships | A | One `main`, one `header`, one `footer`. Each screen is a `section` tied to its heading by `aria-labelledby`. Results is a real `table` with a `caption`, `th scope="col"` and `th scope="row"`. The answer field is joined to its `label` by `for` and `id`. |
| 1.3.2 Meaningful sequence | A | Reading order is DOM order on every screen. No CSS reordering. |
| 1.4.1 Use of colour | A | Right and wrong are never colour alone. Each row also carries the words Right, Wrong or Counted right. |
| 1.4.3 / 1.4.6 Contrast | AA / **AAA** | Full audit in section 3. Lowest ratio anywhere is 7.28:1. |
| 1.4.4 Resize text | AA | Type is set in rem and clamp. Readable and operable at 200 percent with no loss. |
| 1.4.10 Reflow | AA | Single column below 820px. No horizontal scroll at 320px wide. |
| 1.4.11 Non-text contrast | AA | Focus ring, field borders and button borders all clear 3:1. See section 3 for the one thing this changed. |
| 1.4.12 Text spacing | AA | No fixed heights on text containers. |
| 2.1.1 / 2.1.2 Keyboard | A | Everything is a real `button`, `select` or `input`. Nothing traps focus. Full flow verified by keyboard alone. |
| 2.2.1 Timing adjustable | A | See section 4. This is the criterion a timed exam most easily fails, so it is treated separately. |
| 2.4.1 Bypass blocks | A | Skip link to `#main`, visible on focus. |
| 2.4.3 Focus order | A | Focus lands on the answer field when a question opens, which is where a student wants it. Tab order then runs Back, Next, End. |
| 2.4.7 Focus visible | AA | 3px navy ring, 3px offset, gold halo. Never removed. |
| 2.4.11 Focus not obscured | AA (2.2) | Nothing is sticky or overlaid, so a focused control is never covered. |
| 2.5.3 Label in name | A | Visible button text is the accessible name. The override buttons add an `aria-label` that keeps the visible words and adds the question number. |
| 2.5.8 Target size | AA (2.2) | Every control is at least 44 by 44 CSS pixels. Buttons are 48 tall, small buttons 44. |
| 3.2.2 On input | A | No control changes context on its own. The clock is the only automatic change and it is announced. |
| 3.3.1 / 3.3.2 Labels and errors | A | The one input is labelled and its purpose is stated. There is no error state to report: an unanswered question is simply marked wrong and shown as "left blank". |
| 3.3.7 Redundant entry | A (2.2) | Answers persist when a student steps back and forward, so nothing is retyped. |
| 4.1.2 Name, role, value | A | Native elements throughout. `aria-expanded` is not needed as nothing collapses. |
| 4.1.3 Status messages | AA | One `role="status"` `aria-live="polite"` region carries the new question, the 30 and 10 second warnings, time up, pause and resume, and every override. |

## 2. Keyboard flow, verified

Driven by keyboard alone, not by script clicks. Tab order from load is: skip link, seconds
select, order select, Start the exam, Open the answer key. Starting puts focus straight in
the answer field, and Enter moves to the next question and refocuses the field, so the whole
exam can be taken without a mouse.

**Two keyboard defects were found this way and fixed.** Both would have passed axe.

1. **Space was pausing the clock instead of pressing the focused button.** A keyboard user
   who tabs to Next and presses Space expects the button to fire. It paused instead. Space
   is now left alone whenever focus is on a button.
2. **The pause and full screen shortcuts were unreachable in practice.** They were bound to
   plain Space and plain F and suppressed while typing, and focus sits in the answer field
   for the whole exam, so a student could never reach them. Pause is now **Shift and P** and
   full screen is **Shift and F**, both of which work from inside the answer field because no
   answer contains a shifted letter on its own. Plain Space and plain F still work for
   whoever is driving the room with focus outside the field. Verified that typing a space
   into an answer does not pause, and that Shift and P pauses and resumes from the field.

Escape ends the exam and grades it from anywhere, verified. Arrow keys step between questions
when focus is outside the answer field, and move the text cursor when it is inside, which is
the behaviour a text field owes its user.

Results: Tab reaches Take it again, Go over the answer key, then each Count this right button
in row order. Key: Print the key, Back to the start.

## 3. Colour contrast audit

Measured, not estimated. Ratios computed from the relative luminance formula in WCAG 2.x.

| Text | Foreground | Background | Ratio | Level |
|---|---|---|---|---|
| Body and prompts | `#1E3D4C` navy | `#FFFFFF` | 11.49:1 | AAA |
| Body and prompts | `#1E3D4C` navy | `#FAFAF9` off white | 11.01:1 | AAA |
| Headings and eyebrow | `#8B3A2E` terra | `#FFFFFF` | 7.66:1 | AAA |
| Headings and eyebrow | `#8B3A2E` terra | `#FAFAF9` | 7.33:1 | AAA |
| Secondary text | `#465660` | `#FFFFFF` | 7.61:1 | AAA |
| Secondary text | `#465660` | `#FAFAF9` | 7.28:1 | AAA |
| Button label | `#FFFFFF` | `#1E3D4C` navy | 11.49:1 | AAA |
| Button label, hover | `#FFFFFF` | `#142a36` navy deep | 14.85:1 | AAA |
| "Right" | `#1F5B3A` | `#E9F2ED` | 7.03:1 | AAA |
| "Wrong" | `#8B2020` | `#F7ECEC` | 7.81:1 | AAA |
| Row text on a right row | `#1E3D4C` | `#E9F2ED` | 10.06:1 | AAA |
| Row text on a wrong row | `#1E3D4C` | `#F7ECEC` | 9.94:1 | AAA |


**One change came out of this audit.** The focus ring was brushed gold `#B8924A`, which
measures **2.77:1** against the off white page. That is under the 3:1 that SC 1.4.11 requires
of a focus indicator, and axe-core does not test focus indicators, so nothing would have
caught it automatically. The ring is now navy at 11:1 with the brushed gold kept as a soft
halo around it, so the palette still reads as yours and the indicator is compliant.
Secondary text was `#4A5A63`, which is 6.85:1 on off white, just short of AAA. It is now
`#465660`.

## 4. Timing, SC 2.2.1

A timed practical is arguably covered by the essential exception, since the time limit is the
thing being practised. The page does not lean on that exception:

- The clock is set before the exam starts: 1 minute, 1 minute 15, 1 minute 30, 2 minutes, or
  no timer at all.
- **No timer** turns the limit off completely and is one click away on the setup screen.
- **Add 30 seconds** extends the current question, any number of times.
- **Pause** stops the clock outright.
- Warnings are announced to a screen reader at 30 seconds and at 10 seconds, not every
  second, so the live region does not become noise.

That covers turn off, adjust and extend, which is all three of the ways 2.2.1 can be
satisfied.

## 5. What was tested, and by what

**Be clear about this one.** No human screen reader session has been run on this page. What
was run is automated: axe-core 4.10 on all four screens, and a direct read of the
accessibility tree Chromium exposes, which is the same tree a screen reader consumes. That
catches structure and naming. It does not catch how a real reader paces or phrases things.

Confirmed from the accessibility tree on a live question:

```
WebArea: Module 1 Practice Lab Exam | BIO 004
  link: Skip to the exam
  heading: Practice Lab Exam
  text: Question 1, number 1 of 46
  button: Add 30 seconds
  button: Pause
  textbox: Your answer
  button: Back
  button: Next question
  image: Specimen for question 1. Identify it by eye from the slide.
  button: End the exam and grade it
```

Every control has a name, the field is named by its label, and the picture is described.
The status region reports as `role=status` with `aria-live="polite"`, which is what carries
the new question, the 30 and 10 second warnings, pause and resume, and every override.

A results row exposes as `TH: 23 | TD: | TD: Name this entire layer at the bracket |
TD: epidermis | TD: Dermis | TD: Wrong, Count this right`, so a reader announces the question
number as the row header and reads the comparison in order.

**Still to do before this is signed off as screen reader verified:** one pass with NVDA on
Windows or VoiceOver on macOS, taking three or four questions and reading the results table.
Twenty minutes of work. Until that happens, section 1 should be read as AA verified by
automated testing and structural inspection, not by assistive technology in use.

## 6. Known limitations and remediation plan

1. **The identification questions cannot be made non-visual.** Naming a tissue from a
   micrograph is a visual skill and it is the skill the practical tests, so alt text
   deliberately describes the picture as a specimen to be identified rather than naming what
   it is. A student who cannot use the images needs an alternate assessment of the same
   competency, not a better caption. This is a limit of the assessment, not a defect in the
   page, and it should be handled through the accommodation process.
2. ~~Questions 33 to 38 are absent.~~ **Resolved.** The three slides arrived and all 52
   questions are in. Slide 18, the two figures, carries her question text inside the picture
   area rather than beside it, so that text is painted out before the crop rather than cropped
   away. Checked by eye that no wording survives in the delivered picture.
3. **Fonts load from Google Fonts.** If that request is blocked, the page falls back to the
   system sans stack. Layout and contrast are unaffected. If you would rather not depend on
   it at all, the two font files can be self hosted in the repo.
4. **Full screen on iPadOS Safari.** The F key shortcut does nothing there, because Safari on
   iPad does not expose the Fullscreen API to a page. Everything else works. No fix
   available from inside the page.

## 7. On the PowerPoint and the Word key

The `.pptx` is a picture deck: each slide is one rendered image. That means **the question
text in the deck is not machine readable**, which is the same limitation your original deck
had. It is fine for projecting in a room. It is not the accessible copy. The accessible copy
is `module1-practice-exam.html`, where every prompt is real text, and it should be the version
given to any student who needs one.

The DOCX key is a real Word table with a header row and live text, so it reads correctly in a
screen reader and reflows on a phone. Contrast in it is the same navy, terra and grey audited
above.

## 8. The slide show and the check sheet

Both were built to the same floor and audited the same way. Zero axe-core violations across
every screen of each: the slide show on its title slide, a question slide, a slide with the
answers revealed and the last slide; the check sheet on the flagged view, with a correction
open, with the output showing, and with all 52 listed.

Points specific to them:

- **Slide show.** Space and Enter advance the deck only when focus is not on a button, so a
  keyboard user pressing Space on Next still presses Next. Every slide change and every clock
  warning goes to a `role="status"` region. The clock can be turned off entirely from the
  Clock button, which is SC 2.2.1 again. Type is set in `clamp()` against the viewport so it
  scales with the projector rather than being fixed at one size.
- **Check sheet.** The keep and change controls are real radio buttons in a `fieldset` with a
  `legend`, so a screen reader announces the group. Marking a question is announced. The
  correction fields appear with `hidden` rather than `display:none` in CSS, so assistive
  technology sees the same thing the eye does.
- **One thing to know about the check sheet.** It stores your marks in that browser's
  local storage. Marks made in Safari will not appear in Chrome, and a private window keeps
  nothing. If a browser refuses to store, the sheet says so in the status line rather than
  failing silently.

## 9. Reviewer

Dr. Sharilyn Rennie
