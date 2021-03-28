import os
import logging

from flask import Flask, g
from conf import DATABASE_PATH

from . import db
from .utils import captions
from . import search
from . import meme

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

    #register blueprints
    app.register_blueprint(search.bp, url_prefix='/api/search/')
    app.register_blueprint(meme.bp, url_prefix='/meme/')

    return app
