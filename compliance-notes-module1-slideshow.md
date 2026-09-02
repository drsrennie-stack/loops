# Accessibility compliance notes: Module 1 Practice Lab Exam slide show

**Project:** BIO 004 Human Anatomy, Fall 2026, Solano Community College
**Files covered:** `module1slideshow.html`
**Date:** September 2, 2026 (restyled into the MedMasters editorial system; no behavior changes)
**Reviewer:** Dr. Sharilyn Rennie (build and automated checks by Claude)

## 1. What this is

The projector slide show for the Module 1 practice lab exam: 26 specimen slides, two questions each, a per-slide clock (cycling presets, pause, low-time warning), answers on demand, and full keyboard operation. This revision converts it from the retired palette (old navy #1E3D4C, old gold #B8924A, DM Sans, green answers) to the current editorial system: navy #0B1530, terra #8B3A2E, gold #C9A14A, Figtree body with Plus Jakarta Sans display, tracked terra eyebrow, a terra emphasis word in the title, uppercase tracked buttons (terra primary, navy for pressed states), answers revealed in terra-dark behind a terra bar (green removed per the course color rules), and the specimen plate floating on a shadow. All timing, navigation, announcement, and answer logic is untouched.

## 2. Compliance

WCAG 2.2 AA met; contrast AAA on text pairs (navy 18:1, terra 7.66:1, terra-dark answers 9.9:1, muted 7.5:1 on white). Buttons are real buttons with visible focus (navy ring with a gold halo), aria-pressed on the toggles, and 44px minimum height; keyboard shortcuts never steal Space/Enter from a focused button. Slide changes, time warnings at 30 and 10 seconds, pause state, and answer visibility are announced through a polite live region; specimen images carry alt text naming their question numbers. Low-time and paused states change text and color together, never color alone. axe-core (wcag2a + wcag2aa) on the title and question views: 0 violations, no console errors.

## 3. Known limitations

- Answers are in the page source, as with every self-run class tool; this is a practice exam projected by the instructor.
- The deck is built for a projector: it deliberately locks page scroll and manages its own layout, so it is not embedded in Canvas and does not carry the dock.
