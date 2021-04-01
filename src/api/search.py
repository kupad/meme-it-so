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

#should this be moved to the episode blueprint?
@bp.route('/ep/<ep>/<int:ms>', methods=(['GET']))
def search_by_time(ep, ms):
    """
    find a matching frame in an episode via the ms offset
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

    fps = epvidinfo['fps']

    #calculate largest frame that is a multiple of nthframe
    lastframe = epvidinfo['nframes'] - 1
    maxframe = lastframe - lastframe % nthframe

    #find the closest frame to the ms offset in the episode
    frame = closest_frame(ms, fps)
    logging.debug(f'search_by_time: ep({ep}) ms({ms}) --> frame({frame})')

    #find the relevant scene in the episode
    #adding in the prev and next scenes into the results
    #it's okay if there is no scene! We'll still display the frames
    scene = db.query_db('''
        WITH ctx as (
            SELECT *,
                    lag(content) over () prev_content,
                    lead(content) over () next_content
                FROM captions
                WHERE episode = ?
        )
        SELECT *
            FROM ctx
            WHERE start_offset <= ? AND ? <= end_offset''', (ep, ms, ms), one=True)
    logging.debug(scene)

    if scene is None:
        logging.info(f"search_by_time: no hits found for ep {ep} ms {ms}")
        rv['msg'] = 'No hits found'

    logging.debug(f'nframes: {epvidinfo["nframes"]}')

    rv = {
        'ep': ep,
        'scene': scene,
        'frame': frame,
        'imgUrl': frame_to_url(ep, frame),
        'fps': fps,
        'title': epvidinfo['title'],
        'maxframe': maxframe,
    }

    return rv
