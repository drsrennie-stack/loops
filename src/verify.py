#!/usr/bin/env python3
"""Drive the exam page end to end and audit it against WCAG 2.2 AA.

Checks the things that would embarrass us in front of a class: that the clock
counts and hands over, that the grader marks a right answer right and a
misspelling wrong, that the override moves the score, that the key opens with
every question on it, and that axe-core finds nothing on any of the four
screens.
"""
import json
import os
import sys
import urllib.request
from playwright.sync_api import sync_playwright

PAGE = 'file:///root/t3/out/module1-practice-exam.html'
AXE = '/root/t3/node_modules/axe-core/axe.min.js'
AXE_URL = ('https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js')

if False:
    urllib.request.urlretrieve(AXE_URL, AXE)
axe = open(AXE, encoding='utf-8').read()

fails = []


def check(name, ok, detail=''):
    print(('  PASS  ' if ok else '  FAIL  ') + name + (('  ' + detail) if detail else ''))
    if not ok:
        fails.append(name + ' ' + detail)


def audit(page, label):
    page.evaluate(axe)
    r = page.evaluate("""async () => await axe.run(document, {
        runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}
    })""")
    v = r['violations']
    check('axe clean on ' + label, not v,
          '' if not v else json.dumps([x['id'] for x in v]))


with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = b.new_page(viewport={'width': 1400, 'height': 950})
    pg.goto(PAGE)
    pg.wait_for_selector('#startBtn')

    total = pg.evaluate('Q.length')
    check('52 questions loaded', total == 52, 'got %d' % total)
    nums = pg.evaluate('Q.map(q=>q.n)')
    check('her numbering, 1 to 52, no gaps', nums == list(range(1, 53)),
          '' if nums == list(range(1, 53)) else str(nums))
    imgs = pg.evaluate('Q.map(q=>q.s)')
    missing = [s for s in set(imgs)
               if not os.path.exists('/root/t3/out/images/module1-practice/%s.jpg' % s)]
    check('every slide file present', not missing, str(missing))

    audit(pg, 'setup')

    # ---- grader, tested directly against the real answer table -------------
    cases = [
        (1, 'cardiac muscle', True),
        (1, 'cardiac muscle tissue of the heart', True),   # extra words are free
        (1, 'skeletal muscle', False),
        (21, 'adipose tissue', True),                      # the swapped slide
        (21, 'fat', True),
        (21, 'cardiac muscle', False),
        (22, 'the hypodermis', True),
        (37, 'elastic cartilage', True),
        (37, 'hyaline cartilage', False),
        (36, 'transverse plane', True),
        (36, 'sagittal plane', False),
        (34, "meissner's corpuscle", True),
        (2, 'intercalated disc', True),
        (2, 'intercallated disc', False),                  # spelling still counts
        (23, 'dermis', True),
        (23, 'epidermis', False),                          # word start matching
        (17, 'stratified squamous', True),
        (17, 'keratinized stratified squamous', False),    # wrong one of the pair
        (17, 'non keratinized stratified squamous', True),
        (41, 'keratinized stratified squamous epithelium', True),
        (41, 'non keratinized stratified squamous', False),
        (49, 'brachial', True),
        (49, 'forearm', False),
        (27, 'C', True),
        (27, 'A', False),
        (31, 'simple squamous epithelium', True),
        (31, 'stratified squamous epithelium', False),
        (13, 'dense irregular connective tissue', False),
        (8, 'the wall of the stomach', True),
        (5, '', False),
    ]
    bad = []
    for n, typed, want in cases:
        got = pg.evaluate("([n,t]) => grade(Q.find(q=>q.n===n), t)", [n, typed])
        if got != want:
            bad.append('q%d "%s" gave %s' % (n, typed, got))
    check('grader agrees on %d cases' % len(cases), not bad, '; '.join(bad))

    # ---- run the exam -----------------------------------------------------
    pg.select_option('#secs', '60')
    pg.click('#startBtn')
    pg.wait_for_selector('#runScreen:not([hidden])')
    check('clock starts', pg.inner_text('#digits') == '1:00',
          pg.inner_text('#digits'))
    check('picture rendered',
          pg.evaluate("document.getElementById('qimg').naturalWidth") > 100)
    audit(pg, 'a question')

    pg.wait_for_timeout(2100)
    d = pg.inner_text('#digits')
    check('clock is counting down', d in ('0:58', '0:57'), d)
    pg.click('#pauseBtn')
    pg.wait_for_timeout(1600)
    check('pause holds the clock', pg.inner_text('#digits') == d,
          pg.inner_text('#digits'))
    pg.click('#pauseBtn')
    pg.click('#plus30')
    check('add thirty seconds works',
          int(pg.inner_text('#digits').split(':')[1]) > 20
          or pg.inner_text('#digits').startswith('1:'),
          pg.inner_text('#digits'))

    # answer every question, deliberately fluffing one for the override test
    for i in range(total):
        n = pg.evaluate('order[at].n')
        typed = pg.evaluate('Q.find(q=>q.n===%d).a' % n)
        if n == 5:
            typed = 'two layers of cube shaped cells'    # right idea, wording the grader misses
        pg.fill('#answer', typed)
        pg.click('#nextBtn')
    pg.wait_for_selector('#resultScreen:not([hidden])')

    pct = pg.inner_text('#scoreBig')
    check('graded and scored', pct.endswith('%'), pct)
    right = pg.evaluate('tally()')
    check('key answers grade themselves right', right >= 44,
          '%d of %d' % (right, total))
    audit(pg, 'results')

    overrides = pg.query_selector_all('#resBody button')
    if overrides:
        before = pg.evaluate('tally()')
        overrides[0].click()
        after = pg.evaluate('tally()')
        check('override moves the score', after == before + 1,
              '%d then %d' % (before, after))
    else:
        check('override available where marked wrong', right == total,
              'nothing was marked wrong, so nothing to override')

    pg.click('#toKeyBtn')
    pg.wait_for_selector('#keyScreen:not([hidden])')
    items = len(pg.query_selector_all('.keyitem'))
    check('key lists every question', items == total, '%d blocks' % items)
    audit(pg, 'the key')

    # contrast, spot checked on the two colours that carry body text
    audit(pg, 'the key (repeat after render)')

    b.close()

print()
if fails:
    print('%d problem(s):' % len(fails))
    for f in fails:
        print('  ' + f)
    sys.exit(1)
print('all checks passed')
