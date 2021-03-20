import functools
import os

from flask import (
    Blueprint, g, request, session, url_for
)

from engif import find_matches, get_season, get_fps, ms2frame

bp = Blueprint('search', __name__, url_prefix='/search')

thumbnails='/static/thumbnails'

@bp.route('/', methods=(['GET']))
def register():
    rv = {}
    query = request.args.get('q')
    rv['q'] = query

    scenes = find_matches(query)
    for scene in scenes:
        ep = scene.ep
        orig_fps = get_fps(ep)
        season = get_season(ep)
        start_frame, end_frame = ms2frame(scene, orig_fps)
        img = f'{thumbnails}/{season}/{ep}/{start_frame:05}.jpg'
        scene['img'] = img

    rv['matches'] = scenes



    return rv
