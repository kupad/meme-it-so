import functools
import os

from flask import (
    Blueprint, g, request, session, url_for
)

from utils.subtitles import find_matches, ms2frame
from utils.episode_utils import get_season
from utils.video_index import get_fps

bp = Blueprint('search', __name__)

thumbnails='/static/thumbnails'

@bp.route('/', methods=(['GET']))
def search():
    rv = {}
    query = request.args.get('q')
    if query is None:
        rv['matches'] = []
        return rv

    scenes = find_matches(query)
    for scene in scenes:
        ep = scene.ep
        orig_fps = get_fps(ep)
        season = get_season(ep)
        start_frame, end_frame = ms2frame(scene, orig_fps)
        repr_frame = start_frame
        img = f'{thumbnails}/{season}/{ep}/{repr_frame:05}.jpg'
        scene['img_url'] = img

    rv['matches'] = scenes



    return rv
