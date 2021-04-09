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
import numpy as np

from .utils.eptools import get_season
from .utils.frames import closest_frame
from .utils.imgtools import add_text

bp = Blueprint('gif', __name__)

nthframe=6 #FIXME: this needs to be make a configurable option

#IMPACT = 'Impact.ttf'

#FIXME: factor out: being used 2x
def ep_to_thumbnail_dir(ep):
    #TODO: confirm that ep is of SxxExx format!!
    season = get_season(ep)
    img_dir = safe_join(current_app.config["THUMBNAILS_DIR"], season, ep)
    return img_dir

@bp.route('/ep/<ep>/<int:start_frame>.<int:end_frame>.gif', methods=(['GET']))
def generate_gif(ep, start_frame, end_frame):
    """
    dynamically generate the gif
    """
    enctxt = request.args.get('txt', '')
    logging.debug("enctxt %s", enctxt)
    txt = base64.urlsafe_b64decode(enctxt).decode('utf-8')
    logging.debug("txt %s", txt)

    #as a precaution: cap end_frame at {maxsecs} seconds max.
    maxsecs = 12 #frontend is enforcing a 10 seconds. gonna be a bit more lax here
    est_fps = 24 #could look this up. but 24 works for this purpse. I just don't wont people manually putting in large numbers
    est_elapsed = (end_frame - start_frame) / est_fps
    if(est_elapsed > maxsecs):
        logging.warning(f'gif: received req that exceeds maxsecs. est_elapsed: {est_elapsed} ep: {ep} start: {start_frame} end: {end_frame}')
        abort()

    #find path to image dir
    img_dir = ep_to_thumbnail_dir(ep)

    #add all relevant image paths
    paths = [ safe_join(img_dir, f'{frame:05}.jpg') for frame in range(start_frame,end_frame+nthframe,nthframe)]
    #TODO: check that images are in path
    logging.debug(paths)

    logging.debug('generating gif...')
    gif_bytes = BytesIO()
    with imageio.get_writer(gif_bytes, mode='I', format='gif', subrectangles=False, fps=5) as writer:
        for path in paths:
            img = np.array(add_text(path,txt)) if txt else imageio.imread(path)
            writer.append_data(img)

    #return it
    gif_bytes.seek(0)
    return send_file(gif_bytes, mimetype='image/gif')
