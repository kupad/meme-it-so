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

# search.py
# Provides endpoints for finding scenes by user queries, and finding frames by offset.
# See: search() as an the first entry point into the app

import logging

from flask import ( Blueprint, g, request, session, url_for )

from . import db
from .utils.frames import repr_img_url

bp = Blueprint('episode', __name__)

pagelen=50

#TODO: rename fields of scene

#should this be moved to the episode blueprint?
@bp.route('/<ep>', methods=(['GET']))
def get_all_scenes(ep):
    """
    return all scenes in the episode
    """
    rv = {}

    page = request.args.get('page', default=1, type=int)

    #TODO: factor out epvidinfo, since used 2x
    #first get video and episode information for the episode.
    epvidinfo = db.query_db('''
        SELECT v.fps, e.title
            FROM video_info v
            INNER JOIN episode_guide e
            using (episode)
            where v.episode = ?''', (ep, ), one=True)

    #if there is no video info for this episode, abandon now
    if epvidinfo is None:
        logging.info(f"episode: get_all_scenes: ep {ep} not found")
        abort()

    fps = epvidinfo['fps']
    title = epvidinfo['title']


    scenes = db.query_db('''
        SELECT *
            FROM captions c
            WHERE episode = ?
            ORDER BY start_offset ASC
            LIMIT ?, ?''', (ep,(page-1)*pagelen,pagelen))
    logging.debug(scenes)

    if scenes is None:
        scenes = []

    #decorate with fps
    for s in scenes:
        s['fps'] = fps

    #decorate with repr_img_url
    for s in scenes:
        s['imgUrl'] = repr_img_url(s)

    rv = {
        'ep' : ep,
        'scenes': scenes,
        'title': title,
        'page': page,
        'hasMore': len(scenes) == pagelen,
    }

    return rv
