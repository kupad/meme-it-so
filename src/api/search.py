"""
Provides endpoints for finding scenes by user queries, and finding frames by offset.
See: search() as an the first entry point into the app
"""

import logging

from flask import ( Blueprint, g, request, session, url_for )

from . import db
from .utils import captions
from utils.episode_utils import get_season

bp = Blueprint('search', __name__)

thumbnails='/static/thumbnails' #base url for thumbnails
nthframe=6 #work with every 6th frame

def closest_frame(ms,fps):
    """returns the closest frame to the time offset"""
    est_frame = round( (ms / 1000) * fps)
    frame = est_frame - (est_frame % nthframe)
    return frame

def repr_frame(scene):
    """returns the frame that represents this scene"""
    return closest_frame(scene['start_offset'], scene['fps'])

def frame_to_url(ep, frame):
    """translates a frame to an img url"""
    season = get_season(ep)
    img_url = f'{thumbnails}/{season}/{ep}/{frame:05}.jpg'
    return img_url

def repr_img_url(scene):
    """return an image_url that will represent this scene"""
    return frame_to_url(scene['ep'], repr_frame(scene))

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

    #query the whoosh index for hits
    hits = captions.query(q)
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
    rv['matches'] = rows
    return rv

@bp.route('/ep/<ep>/<int:ms>', methods=(['GET']))
def search_by_time(ep, ms):
    """
    find a matching frame in an episode via the ms offset
    """
    rv = {}

    #first get video and episode information for the episode.
    epvidinfo = db.query_db('''
        SELECT v.fps, e.title
            FROM video_info v
            INNER JOIN episode_guide e
            using (episode)
            where v.episode = ?''', (ep, ), one=True)

    #if there is no video info for this episode, abandon now
    if epvidinfo is None:
        logging.info(f"search_by_time: no hits found for ep {ep} ms {ms}")
        abort()

    fps = epvidinfo['fps']
    title = epvidinfo['title']

    #find the closest frame to the ms offset in the episode
    frame = closest_frame(ms, fps)
    logging.debug(f'search_by_time: ep({ep}) ms({ms}) --> frame({frame})')

    #find the relevant scene in the episode
    #it's okay if there is no scene! We'll still display the frames
    scene = db.query_db('''
        SELECT *
            FROM captions
            WHERE episode = ? AND start_offset <= ? AND ? <= end_offset''', (ep, ms, ms), one=True)

    if scene is None:
        logging.info(f"search_by_time: no hits found for ep {ep} ms {ms}")
        rv['msg'] = 'No hits found'

    rv['scene'] = scene
    rv['frame'] = frame
    rv['img_url'] = frame_to_url(ep, frame)
    rv['title'] = title
    rv['fps'] = fps
    return rv
