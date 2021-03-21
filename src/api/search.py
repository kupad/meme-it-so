import functools
import os
from math import floor

from flask import (
    Blueprint, g, request, session, url_for
)

from utils.subtitles import find_by_time, find_matches, ms2frame
from utils.episode_utils import get_season
from utils.video_index import get_fps

bp = Blueprint('search', __name__)

thumbnails='/static/thumbnails'
nthframe=6


#should this be a function of the scene itself?
def repr_frame(scene):
    """
    returns the frame that represents this scene
    """
    ep = scene.ep
    orig_fps = get_fps(ep)
    start_frame, end_frame = ms2frame(scene, orig_fps)
    return start_frame

def frame_to_url(ep, frame):
    season = get_season(ep)
    img_url = f'{thumbnails}/{season}/{ep}/{frame:05}.jpg'
    return img_url

def repr_img_url(scene):
    return frame_to_url(scene.ep, repr_frame(scene))

@bp.route('/', methods=(['GET']))
def search():
    rv = {}
    query = request.args.get('q')
    if query is None:
        rv['matches'] = []
        return rv

    scenes = find_matches(query)
    for scene in scenes:
        scene['img_url'] = repr_img_url(scene)

    rv['matches'] = scenes
    return rv

@bp.route('/ep/<ep>/<int:ms>', methods=(['GET']))
def search_by_time(ep, ms):
    rv = {}

    #find the closest frame to the ms offset in the episode
    orig_fps = get_fps(ep)
    est_frame = round( (ms / 1000) * orig_fps)
    frame = est_frame - (est_frame % nthframe)

    #find the relevant scene in the episode
    scene = find_by_time(ep, ms)

    #stop here if we didn't find anything
    rv['scene'] = scene
    if scene is None:
        rv['msg'] = 'No Scene Found'

    rv['frame'] = frame
    rv['img_url'] = frame_to_url(ep, frame)
    return rv
