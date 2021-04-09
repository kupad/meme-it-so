# This file is part of Meme It So
#
# "Meme It So" is a media (TV show and movies) screen capture and text caption
# database and image macro generator.
# Copyright (C) 2021  Phillip Dreizen
#
# Meme It So is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Meme It So is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Tools for manipulating images:
    - adding text to images
"""

import os

from PIL import Image, ImageFont, ImageDraw

IMPACT = 'Impact.ttf'
FALLBACK = 'DejaVuSans-Bold.ttf' #just some attempt to have a free font available.
                                 #consider distributing a free font that is a good IMPACT replacement

#TODO: catch FileNotFoundError when calling this
    #except FileNotFoundError:
    #    abort(404)
def add_text(img_path, txt):

    pil_img=None
    try:
        #read img into memory, then draw on image
        pil_img = Image.open(img_path)
    except FileNotFoundError:
        abort(404)

    margin_bottom = 20 #pixels
    try:
        font = ImageFont.truetype(IMPACT, 32)
    except OSError:
        logging.warning(f'meme.py: looks like {IMPACT} font is not available. Consider installing mstcorefonts. Trying {FALLBACK}')
        try:
            font = ImageFont.truetype(FALLBACK, 32)
        except OSError:
            logging.error(f'meme.py: {FALLBACK} is not available. Need to install {IMPACT} or {FALLBACK}')
            #TODO: return a placeholder error image here
            abort()

    img_w, img_h = pil_img.size
    draw = ImageDraw.Draw(pil_img)
    text_w, text_h = draw.textsize(txt, font)
    textpos = ((img_w - text_w) // 2, img_h - text_h - margin_bottom)
    draw.text(textpos, txt,
        align='center',
        font=font,
        fill='white',
        stroke_width=2,
        stroke_fill='black',
    )

    return pil_img
