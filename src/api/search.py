import functools

from flask import (
    Blueprint, g, request, session, url_for
)

from engif import find_matches

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=(['GET']))
def register():
    rv = {}
    query = request.args.get('q')
    rv['q'] = query

    matches = find_matches(query)
    rv['matches'] = matches


    
    return rv

