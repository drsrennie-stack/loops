#!/usr/bin/env python3
"""Drive the answer check sheet and audit it.

The point of this sheet is that a correction comes back attached to the right
question. So the checks care about two things above all: that marking a
question produces output naming that question and its current key, and that
what she types survives a reload.
"""
import json
import os
import sys
from playwright.sync_api import sync_playwright

PAGE = 'file:///root/t3/out/answer-check-sheet.html'
axe = open('/root/t3/node_modules/axe-core/axe.min.js', encoding='utf-8').read()
fails = []


def check(name, ok, detail=''):
    print(('  PASS  ' if ok else '  FAIL  ') + name + (('  ' + detail) if detail else ''))
    if not ok:
        fails.append(name + ' ' + detail)


def audit(pg, label):
    pg.evaluate(axe)
    r = pg.evaluate("""async () => await axe.run(document, {
        runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}
    })""")
    v = r['violations']
    check('axe clean, ' + label, not v,
          '' if not v else json.dumps([x['id'] for x in v]))


with sync_playwright() as pw:
    b = pw.chromium.launch(
        executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = b.new_context(viewport={'width': 1300, 'height': 950})
    ctx.grant_permissions(['clipboard-read', 'clipboard-write'])
    pg = ctx.new_page()
    pg.goto(PAGE)
    pg.wait_for_selector('#list .q')

    total = pg.evaluate('D.items.length')
    nflag = pg.evaluate('D.items.filter(function(q){return q.flag}).length')
    shown = pg.eval_on_selector_all('#list .q', 'els => els.length')
    # With flags outstanding the sheet opens on just those. With none left it
    # opens on the whole exam, because an empty list would read as broken.
    want = nflag if nflag else total
    check('opens on the right set', shown == want,
          '%d shown, %d flagged of %d' % (shown, nflag, total))
    check('a reason on every flagged card',
          pg.eval_on_selector_all('#list .why', 'e => e.length') == nflag)
    check('the all clear shows only when nothing is flagged',
          pg.eval_on_selector('#allClear', 'e => e.hidden') == (nflag > 0))
    broken = pg.evaluate("""() => Array.from(document.querySelectorAll('#list img'))
        .filter(i => !i.complete || i.naturalWidth < 50).length""")
    check('every picture is embedded and loads', broken == 0, '%d broken' % broken)
    check('every picture has alt text',
          pg.evaluate("""() => Array.from(document.querySelectorAll('#list img'))
              .every(i => (i.alt||'').length > 10)"""))
    audit(pg, 'the flagged view')

    # mark one keep, one change, and fill the change in
    pg.click('#q39 .choice:nth-of-type(2)')
    check('change reveals the fields',
          not pg.eval_on_selector('#q39 .fix', 'e => e.hidden'))
    pg.fill('#a39', 'Dense irregular connective tissue')
    pg.fill('#alt39', 'dense irregular CT, irregular connective tissue')
    pg.fill('#n39', 'it is the submucosa')
    pg.click('#q37 .choice:nth-of-type(1)')
    check('keep hides the fields',
          pg.eval_on_selector('#q37 .fix', 'e => e.hidden'))
    txt = pg.inner_text('#count')
    check('counter tracks marks', '2 of' in txt or '2 ' in txt, txt)
    audit(pg, 'with a change open')

    # survives a reload
    pg.reload()
    pg.wait_for_selector('#list .q')
    kept = pg.eval_on_selector('#a39', 'e => e.value')
    check('marks survive a reload',
          kept == 'Dense irregular connective tissue', repr(kept))

    # the output
    pg.click('#copyBtn')
    out = pg.eval_on_selector('#out', 'e => e.value')
    print('\n--- what she would paste back ---\n' + out + '\n---')
    check('output names the question and the old key',
          'Q39  CHANGE' in out and 'was:    Elastic connective tissue' in out)
    check('output carries her new answer and note',
          'Dense irregular connective tissue' in out and 'it is the submucosa' in out)
    check('a keep comes through with its key',
          'Q37  KEEP  (Elastic cartilage)' in out)
    check('the corrected question 4 reads collagen now',
          pg.evaluate("D.items.find(function(q){return q.n===4}).a") == 'Collagen fiber',
          pg.evaluate("D.items.find(function(q){return q.n===4}).a"))
    check('untouched questions stay out of it', 'Q1 ' not in out and 'Q46' not in out)
    audit(pg, 'with the output showing')

    # the full list
    if nflag:
        pg.click('#toggleAll')
        all_shown = pg.eval_on_selector_all('#list .q', 'els => els.length')
        check('toggle shows all %d' % total, all_shown == total, '%d shown' % all_shown)
        check('marks survive the toggle',
              pg.eval_on_selector('#a39', 'e => e.value')
              == 'Dense irregular connective tissue')
    else:
        check('the toggle is hidden when there is nothing to filter to',
              pg.eval_on_selector('#toggleAll', 'e => e.hidden'))
    audit(pg, 'all %d showing' % total)

    # keyboard: the radios must be reachable and operable
    pg.evaluate("document.querySelector('#q33 input[type=radio]').focus()")
    pg.keyboard.press('ArrowRight')
    check('radios work from the keyboard',
          pg.evaluate("(state['33']||{}).mark === 'change'"),
          str(pg.evaluate("state['33']")))

    b.close()

print()
if fails:
    print('%d problem(s):' % len(fails))
    for f in fails:
        print('  ' + f)
    sys.exit(1)
print('all checks passed')
