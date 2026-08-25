# Practice Lab Exam, back in the Loops app

Built 25 August 2026. Lives inside `index.html`, no new files.

## What a student does

1. Opens **Practice lab exam**, the first card under Study tools.
2. Ticks whichever loops they are studying. Loops are grouped by module, each one shows how
   many graded questions it holds, and each module has **Select all** and **Clear**.
   The running total tells them how many questions are available before they commit.
3. Sets the length (20, 30, 40 or **52**, the default) and the clock
   (No timer, 30, **45**, 60 or 90 seconds; 45 is the default).
4. Sits the exam. One picture, one countdown, type the answer, next. Nothing is marked and
   no key is shown until the whole thing is finished, the way the real practical works.
   When the clock runs out the question is taken as answered and it moves on.
   **Finish and mark it** ends early; anything not reached counts as missed.
5. Gets the score, the percent, their running average, and their best, then a question by
   question review with the picture, what they typed, and the key.

Every run draws a fresh random set, so no two attempts are the same.

## The override, and what it is for

Auto-marking is not a good judge of wording. A student who writes *simple squamous
epithelial tissue* where the key says *Simple Squamous Epithelium* is not wrong, and the
grader will not see that. So every missed question carries **Count this one right**, which
adds the mark and updates the saved attempt. Pressing it again undoes it.

Two things this is deliberately not:

- It is **not for spelling**. The grader already forgives close spelling by default, so a
  slip never costs a mark and never needs an override. If you want spelling to count on a
  run, tick **Spelling counts** on the setup screen and the grader turns strict.
- It does not appear on questions the grader already marked correct.

## Scoring

One question is one station and is worth one mark. A station with two or three blanks needs
all of them to score. The review shows a tick or a cross beside each blank, so a student can
see they got the tissue but missed the location. If you would rather score per blank, say so
and it is a small change.

## Saved attempts

Every attempt is stored in the browser under `loopsExam_v1`: the date, which loops were
picked, the score, and what was typed. The setup screen shows the whole run of attempts,
newest first, with the average across all of them, the best, and the most recent.
**Clear my exam history** wipes it, two taps.

This is separate from `loopsEngine_v1`, the loop practice record. Exam attempts do not touch
weakness scores, the progress dashboard, or spaced practice, and clearing one does not touch
the other. If you would like a missed exam question to feed **Drill my weak stations**, that
is a one line change; it was left out because it would rewrite practice data you already have.

Nothing is sent anywhere. No names, no accounts, same as the rest of the app.

## Accessibility

Verified with axe-core against WCAG 2.2 AA on all four screens: setup, running, results, and
setup with history. Zero violations. Every colour pair clears 7:1. Full keyboard operation,
including Enter to move down the blanks and on to the next question. The countdown itself is
hidden from screen readers, with a single spoken warning at ten seconds rather than a tick
every second. **No timer** is offered so the time limit can be turned off entirely, which is
what WCAG 2.2.1 asks for.

## If you want the numbers changed

Defaults sit at the top of the exam script: question counts in the `exN` select, clock values
in `exSecs`, and `KEEP` for how many attempts are stored (40).

Dr. Sharilyn Rennie
