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
import logging
import os
import base64
import urllib
from io import BytesIO

from flask import ( current_app, Blueprint, request, send_from_directory, send_file, safe_join, abort )
from PIL import Image, ImageFont, ImageDraw

from .utils.eptools import get_season

bp = Blueprint('meme', __name__)

#nthframe=6

IMPACT = 'Impact.ttf'

def ep_to_thumbnail_dir(ep):
    #TODO: confirm that ep is of SxxExx format!!
    season = get_season(ep)
    img_dir = safe_join(current_app.config["THUMBNAILS_DIR"], season, ep)
    return img_dir

@bp.route('/<ep>/<int:frame>.jpg', methods=(['GET']))
def generate_meme(ep, frame):
    """
    dynamically generate the meme
        potentially: store the meme on disk and cron will kill cached ones
        that haven't been accessed in a while?
    """
    enctxt = request.args.get('txt', '')
    #txt = urllib.parse.unquote(base64.standard_b64decode(enctxt).decode('utf-8'))
    #txt = urllib.parse.unquote(enctxt)
    txt = base64.urlsafe_b64decode(enctxt).decode('utf-8')
    logging.debug(txt)

    #find path to image
    img_dir = ep_to_thumbnail_dir(ep)
    img_name = f'{frame:05}.jpg'
    img_path = safe_join(img_dir, img_name)

    pil_img=None
    try:
        #read img into memory, then draw on image
        pil_img = Image.open(img_path)
    except FileNotFoundError:
        abort(404)

    margin_bottom = 20 #pixels
    font = ImageFont.truetype(IMPACT, 32)
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

    #save image in memory
    img_bytes = BytesIO()
    pil_img.save(img_bytes, 'JPEG', quality=95)
    img_bytes.seek(0)

    #return it
    return send_file(img_bytes, mimetype='image/jpeg')
