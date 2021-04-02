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
from moviepy.editor import *
from PIL import Image

from .utils.eptools import get_season
from .utils.frames import closest_frame

bp = Blueprint('gif', __name__)

nthframe=6 #FIXME: this needs to be make a configurable option

#IMPACT = 'Impact.ttf'

#FIXME: factor out: being used 2x
def ep_to_thumbnail_dir(static_folder, ep):
    #TODO: confirm that ep is of SxxExx format!!
    season = get_season(ep)
    img_dir = os.path.join(static_folder, 'thumbnails', season, ep)
    return img_dir

@bp.route('ping', methods=(['GET']))
def ping():
    return 'pong'

@bp.route('/ep/<ep>/<int:start_ms>.<int:end_ms>.gif', methods=(['GET']))
def generate_gif(ep, start_ms, end_ms):
    """
    dynamically generate the gif
        potentially: store the meme on disk and cron will kill cached ones
        that haven't been accessed in a while?
    """
    #enctxt = request.args.get('txt', '')
    #txt = urllib.parse.unquote(base64.standard_b64decode(enctxt).decode('utf-8'))
    #txt = urllib.parse.unquote(enctxt)
    #txt = base64.urlsafe_b64decode(enctxt).decode('utf-8')
    #logging.debug(txt)
    fps = 24
    start_frame = closest_frame(start_ms, fps)
    end_frame = closest_frame(end_ms, fps)

    #TODO: as a precaution: cap end_frame at 10 seconds max

    #find path to image dir
    img_dir = ep_to_thumbnail_dir(current_app.static_folder,ep)

    #add all relevant image paths
    paths = [ safe_join(img_dir, f'{frame:05}.jpg') for frame in range(start_frame,end_frame+nthframe,nthframe)]
    #TODO: check that images are in path
    logging.debug(paths)

    gif_bytes = BytesIO()

    with imageio.get_writer(gif_bytes, mode='I', format='gif') as writer:
        for path in paths:
            writer.append_data(imageio.imread(path))

    #return it
    gif_bytes.seek(0)
    return send_file(gif_bytes, mimetype='image/gif')
    
