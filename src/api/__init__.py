import os

from flask import Flask, g

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    @app.route('/api')
    def api():
        return {'msg': 'meme-it-so api'}


    from . import search
    app.register_blueprint(search.bp, url_prefix='/api/search/')

    from . import meme
    app.register_blueprint(meme.bp, url_prefix='/meme/')

    return app
