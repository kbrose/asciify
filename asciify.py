# -*- coding: utf-8 -*-

from __future__ import division

import sys
import cgi
from PIL import Image
import numpy as np

# chars = ' .,-:;irosOXA253hMHGS#9B&@'
CHARS = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
CHARS = np.asarray(list(CHARS))

def asciify(image_or_filename,
            width,
            brightness,
            height_multiplier=0.7245,
            chars=CHARS,
            to='html',
            fontsize=8):
    try:
        img = Image.open(image_or_filename)
    except AttributeError:
        img = image_or_filename
    img.size
    S = (int(round(width)), int(round(width * height_multiplier) * (img.size[1] / img.size[0])))
    img = np.sum(np.asarray(img.resize(S)), axis=2)
    img -= img.min()
    img = ((1.0 - img/float(img.max())) ** brightness) * (len(chars)-1)
    img = img.astype(int)

    if to == 'html':
        txt = '<div style="text-align:center">{}</div>'
        txt = txt.format('<pre style="font-size:{}; line-height: 1;">{}</pre>')
        txt = txt.format(
            fontsize,
            cgi.escape("\n".join(("".join(r) for r in chars[img])))
        )
    elif to == 'ascii':
        txt = '\n'.join(("".join(r) for r in chars[img]))
    else:
        raise ValueError('Input "to" must be one of "html" or "ascii"')

    return txt

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python asciify.py image width brightness height-multiplier');
        sys.exit()
    f, SC, B, H = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    print(asciify(f, SC, B, H, to='ascii'))
