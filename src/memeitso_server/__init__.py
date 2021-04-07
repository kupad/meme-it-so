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

import os
import logging

from flask import Flask, g

from . import db
from .utils import srttools
from .utils import captions
from .utils import vidtools

from . import search
from . import meme
from . import gif
from . import episode

def create_app(test_config=None):
    logging.basicConfig(level=logging.DEBUG)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    #override by creating 'application.cfg' and placing in the instance dir
    app.config.from_mapping(
        #override
        SECRET_KEY = 'dev',

        #These are the most likely to be overridden, since where people
        #keep the source video files are what is most likely to change
        SRT_DIR            = os.path.join(app.instance_path, 'srt'),
        VIDEO_DIR          = os.path.join(app.instance_path, 'video'),

        #and might likely to want to move where the thumbnails are stored
        #keep in mind: this is not the URL to the thumbnails, but how the server
        #finds the thumbnails
        THUMBNAILS_DIR     = os.path.join(app.static_folder, 'thumbnails'),

        #TODO: small, mid, large thumbs
        GIF_WIDTH          = 480,
        GIF_HEIGHT         = 356,

        DATABASE           = os.path.join(app.instance_path, 'memeitso.db'),
        CAPTION_INDEX_DIR  = os.path.join(app.instance_path, 'caption_index'),
        EPISODE_GUIDE_PATH = os.path.join(app.instance_path, 'episode_guide.csv'),
        VIDEO_META_PATH    = os.path.join(app.instance_path, 'video_meta.csv'),
        SRT_CSV_PATH       = os.path.join(app.instance_path, 'subtitles.csv'),
        DEFAULT_VIDEO_FPS  = 23.976023976023978,

    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('application.cfg', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #register hooks and cli commands
    srttools.init_app(app)
    db.init_app(app)
    captions.init_app(app)
    vidtools.init_app(app)

    #register blueprints
    app.register_blueprint(search.bp, url_prefix='/api/search/')
    app.register_blueprint(episode.bp, url_prefix='/api/episode/')
    app.register_blueprint(meme.bp, url_prefix='/api/meme/')
    app.register_blueprint(gif.bp, url_prefix='/api/gif/')

    # a simple page that pings back
    @app.route('/api/ping')
    def hello():
        rv = {'msg': '...pong'}
        return rv

    return app
