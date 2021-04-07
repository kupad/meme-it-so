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
from .utils import captions
from .utils.frames import nthframe, closest_frame, repr_img_url, frame_to_url
from .utils.eptools import get_season


bp = Blueprint('search', __name__)

@bp.route('/', methods=(['GET']))
def search():
    """
    This is the workhorse and entry method for the whole application.
    Query the database for scenes that match the query.
    This uses whoosh, via the captions module, as a full-text-search index.
    It will return row ids for matching captions
    """
    rv = {}

    #get the query string. abandon if there is nothing
    q = request.args.get('q')
    if q is None:
        rv['matches'] = []
        return rv

    reqpage = request.args.get('page', default=1, type=int)

    #query the whoosh index for hits
    hits, respage, pagecount = captions.query_page(q, reqpage)
    #logging.debug(hits)

    #map the hits to just the db caption ids
    ids = [ hit['id'] for hit in hits]

    #build an sqlquery to find rows with the same ids
    #joins with video_info since we need the fps information
    sqlquery = """
        SELECT c.*, v.fps
            FROM captions c
            INNER JOIN video_info v
            using (episode)
            WHERE c.id in ({0})
        """.format(', '.join('?' for _ in ids))

    #find matching db rows
    rows = db.query_db(sqlquery, ids)

    #add in an img_url field
    #FIXME: also doing some renaming here. Not good!
    for row in rows:
        row['ep'] = row['episode'] #HACK! FIXME
        row['start'] = row['start_offset'] #HACK! FIXME
        row['end'] = row['end_offset'] #HACK! FIXME
        row['img_url'] = repr_img_url(row)

    #return matches
    rv['hits'] = rows
    rv['page'] = respage
    rv['pageCount'] = pagecount
    return rv

@bp.route('/ep/<ep>/<int:ms>', methods=(['GET']))
def search_by_time(ep, ms):
    """
    Find a matching frame in an episode via the ms offset
    Returns the matching subtitle information for the matching frame if available,
    Also returns the surrounding subtitle inforation, even if no subtitles at this particular offset
    """
    logging.debug(f'ep: {ep} ms: {ms}')
    rv = {}

    #first get video and episode information for the episode.
    epvidinfo = db.query_db('''
        SELECT v.*, e.title
            FROM video_info v
            INNER JOIN episode_guide e
            using (episode)
            where v.episode = ?''', (ep, ), one=True)

    #if there is no video info for this episode, abandon now
    if epvidinfo is None:
        logging.info(f"search_by_time: no hits found for ep {ep} ms {ms}")
        abort()

    logging.debug(f'epvidinfo: {epvidinfo}')

    fps = epvidinfo['fps']

    #calculate largest frame that is a multiple of nthframe
    lastframe = epvidinfo['nframes'] - 1
    maxframe = lastframe - lastframe % nthframe

    #find the closest frame to the ms offset in the episode
    frame = closest_frame(ms, fps)
    logging.debug(f'search_by_time: ep({ep}) ms({ms}) --> frame({frame})')

    #find the relevant scene, along with the previous scene and next scene.
    #For now, doing this in a straightforward way: 3 sql queries...

    #first find the scene
    #it's okay if we don't find anything!
    scene = db.query_db('''
        SELECT *
            FROM captions
            WHERE episode = ?
            AND start_offset <= ? AND ? <= end_offset''', (ep, ms, ms,), one=True)

    if scene:
        logging.debug(f'scene: {scene}')
    else:
        logging.debug(f"search_by_time: no hits found for ep {ep} ms {ms}")

    #boundaries for finding prev and next scenes
    #if we found a scene, the boundary is the start and end of the scene.
    #otherwise it's just the time we received
    start_bound = scene['start_offset'] if scene else ms
    end_bound = scene['end_offset'] if scene else ms

    #prev_scene is the scene with the largest start_offset smaller then start boundary
    prev_scene = db.query_db('''
        SELECT max(start_offset), *
            FROM captions
            WHERE episode = ?
            AND start_offset < ?''', (ep, start_bound), one=True)
    logging.debug(f'prev_scene: {prev_scene}')

    #next_scene is the scene with the smallest end_offset larger than the end boundary
    next_scene = db.query_db('''
        SELECT min(end_offset), *
            FROM captions
            WHERE episode = ? AND
            end_offset > ?''', (ep, end_bound), one=True)
    logging.debug(f'next_scene: {next_scene}')


    rv = {
        'ep': ep,
        'prevScene': prev_scene,
        'scene': scene,
        'nextScene': next_scene,
        'frame': frame,
        'imgUrl': frame_to_url(ep, frame),
        'fps': fps,
        'title': epvidinfo['title'],
        'maxframe': maxframe,
    }

    return rv
