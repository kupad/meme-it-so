from flask import (
    Blueprint, g, request, session, url_for
)

import utils.captions as captions
from utils.video_index import read_video_index
from utils.subtitles import find_by_time, ms2frame
from utils.episode_utils import get_season

bp = Blueprint('search', __name__)

thumbnails='/static/thumbnails'
nthframe=6

video_index = read_video_index()

#should this be a function of the scene itself?
def repr_frame(scene):
    """
    returns the frame that represents this scene
    """
    ep = scene['ep']
    orig_fps = video_index[ep]['fps']
    start_frame, end_frame = ms2frame(scene, orig_fps)
    return start_frame

def frame_to_url(ep, frame):
    season = get_season(ep)
    img_url = f'{thumbnails}/{season}/{ep}/{frame:05}.jpg'
    return img_url

def repr_img_url(scene):
    return frame_to_url(scene['ep'], repr_frame(scene))

@bp.route('/', methods=(['GET']))
def search():
    rv = {}
    q = request.args.get('q')
    if q is None:
        rv['matches'] = []
        return rv

    hits = captions.query(q)
    for scene in hits:
        scene['img_url'] = repr_img_url(scene)

    rv['matches'] = hits
    return rv

@bp.route('/ep/<ep>/<int:ms>', methods=(['GET']))
def search_by_time(ep, ms):
    rv = {}

    if not ep in video_index:
        abort()

    video_info = video_index[ep]

    #find the closest frame to the ms offset in the episode
    orig_fps = video_info['fps']
    est_frame = round( (ms / 1000) * orig_fps)
    frame = est_frame - (est_frame % nthframe)

    #find the relevant scene in the episode
    #TODO: change to use the caption index
    scene = find_by_time(ep, ms)

    #stop here if we didn't find anything
    rv['scene'] = scene
    if scene is None:
        rv['msg'] = 'No Scene Found'

    rv['frame'] = frame
    rv['img_url'] = frame_to_url(ep, frame)
    rv['title'] = video_info['title']
    return rv
