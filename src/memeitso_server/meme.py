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
from .utils.imgtools import add_text

bp = Blueprint('meme', __name__)

#nthframe=6

def ep_to_thumbnail_dir(ep):
    #TODO: confirm that ep is of SxxExx format!!
    season = get_season(ep)
    img_dir = safe_join(current_app.config["THUMBNAILS_DIR"], season, ep)
    return img_dir

@bp.route('/<ep>/<int:frame>.jpg', methods=(['GET']))
def generate_meme(ep, frame):
    """
    dynamically generate the meme
    """
    enctxt = request.args.get('txt', '')
    txt = urllib.parse.unquote(base64.urlsafe_b64decode(enctxt).decode('utf-8'))
    logging.debug(txt)

    #find path to image
    img_dir = ep_to_thumbnail_dir(ep)
    img_name = f'{frame:05}.jpg'
    img_path = safe_join(img_dir, img_name)
    logging.debug(f'meme opening {img_path}')

    try:
        pil_img = add_text(img_path, txt)
    except FileNotFoundError:
        logging.exception('FNF when adding text to path %s', img_path)
        abort(404)

    #save image in memory
    img_bytes = BytesIO()
    pil_img.save(img_bytes, 'JPEG', quality=95)
    img_bytes.seek(0)

    #return it
    return send_file(img_bytes, mimetype='image/jpeg')
