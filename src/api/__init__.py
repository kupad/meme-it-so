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
from conf import DATABASE_PATH

from . import db
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

    app.config.from_mapping(
        SECRET_KEY='dev',
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        DATABASE=DATABASE_PATH
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #register hooks and cli commands
    db.init_app(app)
    captions.init_app(app)
    vidtools.init_app(app)

    #register blueprints
    app.register_blueprint(search.bp, url_prefix='/api/search/')
    app.register_blueprint(episode.bp, url_prefix='/api/episode/')
    app.register_blueprint(meme.bp, url_prefix='/meme/')
    app.register_blueprint(gif.bp, url_prefix='/gif/')

    return app
