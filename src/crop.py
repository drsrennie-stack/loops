#!/usr/bin/env python3
"""Take Dr. Rennie's quiz slides and keep only the picture.

Each slide is 1920x1080: her typed question text sits in white space on one
side, the specimen photograph on the other, and an arrow or bracket bridges
the two. The text is being replaced by real HTML text on the quiz page, so it
has to come off the picture. Arrows and brackets must stay, because several
questions point at them.

Finding the photograph by darkness alone fails on the pale slides (the alveoli
field is mostly white). So each pixel is scored on two things: ink, meaning
darker than near-white, and texture, meaning it differs from its own
neighbourhood. A photograph is textured everywhere, even in its white gaps,
because of film grain and JPEG noise. Flat slide background is neither. A
column of the photograph therefore scores down most of its height, while a
column of typed text scores on a few dozen rows only, so the photograph is the
widest run of columns clearing a threshold.

Brackets and letter labels that stand in the white margin outside the
photograph would be dropped by that rule, so the slides carrying them get a
hand-set widening.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

UP = '/root/.claude/uploads/35994a8e-d21d-5098-8bed-529672064202'
OUT = '/root/t3/out/images/module1-practice'

# slide number -> uploaded file.
SLIDES = {
    1:  'f65554a4', 2:  '3fb78b11', 3:  'fd0d8266', 4:  'b5372547',
    5:  '3131b9c4', 6:  '746d9ddf', 7:  'fa12e7aa', 8:  'bb34beb2',
    9:  '26d7e665', 10: '9b6a5331', 11: '041eb912', 12: '23552335',
    13: '2ac77214', 14: 'c4c455c1', 15: '2879c9b1', 16: '23a9b8ce',
    17: 'aa1a525e', 18: '25d8403a', 19: '45665e26',
    20: 'dbd1c7f6', 21: '7a5b6a7e', 22: '7be3eb46', 23: '5b84f274',
    24: 'c6e15708', 25: '6c991f12', 26: '035b4bb0',
}

# Marks standing in the white margin, outside the photograph itself, plus
# arrowheads that sit right on the picture's edge and would otherwise be
# shaved off. slide -> (extra pixels left, extra pixels right)
WIDEN = {
    4:  (55, 0),    # arrowhead on the smooth muscle
    17: (40, 0),    # arrowhead on the dermal papilla
    19: (40, 0),    # arrowhead on the cartilage
    11: (75, 0),    # arrowhead on the cardiac muscle
    12: (75, 0),    # "ID this entire layer" bracket, left of the skin model
    20: (70, 0),    # arrowhead on the wavy fibre band
    22: (0, 120),   # "Name this Region" bracket, right of the skin model
    24: (70, 0),    # the two arrowheads on the thick skin
    25: (230, 0),   # the A and B arrows and letters, left of the figure
}

# Three pale slides defeat the automatic bounds: the duct, the transitional
# epithelium and the alveoli are mostly white, so the run of textured columns
# breaks up inside the picture. Hand-set on the 1920x1080 slide.
BOX = {
    3:  (665, 40, 1910, 1045),
    18: (0, 0, 1920, 1080),   # both figures, and the A label in the far corner
    13: (630, 0, 1920, 1080),
    16: (735, 0, 1920, 1080),
}

# Slide 18 puts the A label in the top left corner and her question text in the
# left margin below it, so neither side can simply be cropped away. Her text is
# painted out instead and the whole frame kept.
MASK = {
    18: [(60, 555, 530, 700), (60, 805, 1150, 995)],
}

# Labels printed on the specimen that give an answer away. Painted over after
# the crop, in the cropped picture's own coordinates. A flat cover rather than
# cloned tissue: inventing plausible histology inside a slide students are
# asked to read from would be a lie told in the one place it matters most.
# slide -> list of boxes
COVER = {
    2: [(365, 578, 668, 784)],   # the EF and CF labels and their two arrows
}

MAXW = 1100        # cap the delivered width


def score_map(im):
    """Per pixel: is this ink, or is it textured? Either counts."""
    g = im.convert('L')
    a = np.asarray(g, dtype=np.float32)
    blur = np.asarray(g.filter(ImageFilter.GaussianBlur(2)), dtype=np.float32)
    ink = a < 238
    texture = np.abs(a - blur) > 2.5
    return ink | texture


def widest_run(counts, floor, gap):
    """Widest run of indices at or above floor, tolerating short gaps."""
    best, bi, bj = 0, 0, len(counts) - 1
    i, n = 0, len(counts)
    while i < n:
        if counts[i] < floor:
            i += 1
            continue
        j, k = i, i
        while k < n:
            if counts[k] >= floor:
                j, k = k, k + 1
            else:
                run = 0
                while k < n and counts[k] < floor:
                    run += 1
                    k += 1
                if run > gap:
                    break
        if j - i > best:
            best, bi, bj = j - i, i, j
        i = max(k, i + 1)
    return bi, bj


def main():
    os.makedirs(OUT, exist_ok=True)
    for n, stem in sorted(SLIDES.items()):
        im = Image.open(os.path.join(UP, stem + '-image.jpg')).convert('RGB')
        w, h = im.size
        if n in MASK:
            d = ImageDraw.Draw(im)
            for b in MASK[n]:
                d.rectangle(b, fill=(255, 255, 255))

        if n in BOX:
            box = BOX[n]
        else:
            m = score_map(im)
            cols = m.sum(axis=0)
            x0, x1 = widest_run(cols, h * 0.40, gap=40)
            dl, dr = WIDEN.get(n, (0, 0))
            x0 = max(0, x0 - dl)
            x1 = min(w - 1, x1 + dr)

            band = m[:, x0:x1 + 1]
            rows = band.sum(axis=1)
            y0, y1 = widest_run(rows, (x1 - x0) * 0.40, gap=40)
            if y1 - y0 < h * 0.35:
                y0, y1 = 0, h - 1

            pad = 6
            box = (max(0, x0 - pad), max(0, y0 - pad),
                   min(w, x1 + 1 + pad), min(h, y1 + 1 + pad))
        out = im.crop(box)
        if out.width > MAXW:
            out = out.resize((MAXW, round(out.height * MAXW / out.width)),
                             Image.LANCZOS)
        # After the resize, not before. These boxes were measured on the
        # delivered picture, and covering first then scaling moved the patch
        # off the thing it was covering.
        for c in COVER.get(n, []):
            cd = ImageDraw.Draw(out)
            cd.rounded_rectangle(c, radius=10, fill=(255, 255, 255),
                                 outline=(215, 221, 224), width=2)
        path = os.path.join(OUT, 's%02d.jpg' % n)
        out.save(path, 'JPEG', quality=84, optimize=True, progressive=True)
        print('s%02d  box=%-26s out=%4dx%-4d %3dKB'
              % (n, str(box), out.width, out.height,
                 os.path.getsize(path) // 1024))


if __name__ == '__main__':
    main()
