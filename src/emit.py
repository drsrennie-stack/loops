#!/usr/bin/env python3
"""Push the one question table out to everything that consumes it.

questions.json feeds the answer key document. The same list is written into
module1-practice-exam.html between the two sentinel comments, so the timed
runner, the key it prints and the Word key can never drift apart.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data  # noqa: E402

OUT = '/root/t3/out'

payload = {
    'title': data.TITLE,
    'course': data.COURSE,
    'school': data.SCHOOL,
    'byline': data.BYLINE,
    'pending': data.PENDING,
    'questions': data.QUESTIONS,
}
with open(os.path.join(OUT, 'questions.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, indent=1, ensure_ascii=False)

# --- rewrite the array inside the page -------------------------------------
lines = []
for q in data.QUESTIONS:
    bits = ['n:%d' % q['n'], 's:"%s"' % q['s'],
            'tag:%s' % json.dumps(q['tag'], ensure_ascii=False),
            'a:%s' % json.dumps(q['a'], ensure_ascii=False),
            'alt:%s' % json.dumps(q.get('alt', []), ensure_ascii=False),
            'core:%s' % json.dumps(q['core'], ensure_ascii=False)]
    if q.get('no'):
        bits.append('no:%s' % json.dumps(q['no'], ensure_ascii=False))
        bits.append('yes:%s' % json.dumps(q.get('yes', []), ensure_ascii=False))
    lines.append(' {' + ', '.join(bits) + '}')

js = ('var Q = [\n' + ',\n'.join(lines) + '\n];\n\n'
      'var PENDING = ' + json.dumps(data.PENDING) + ';\n')

page = os.path.join(OUT, 'module1-practice-exam.html')
src = open(page, encoding='utf-8').read()
new, n = re.subn(r'/\* QSTART \*/.*?/\* QEND \*/',
                 '/* QSTART */\n' + js + '/* QEND */',
                 src, flags=re.S)
if n != 1:
    raise SystemExit('sentinels not found in %s' % page)
open(page, 'w', encoding='utf-8').write(new)
print('questions.json and the page both carry %d questions'
      % len(data.QUESTIONS))
