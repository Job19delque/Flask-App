# Here it has the App factory
# It should be treated as a package

import os
from flask import Flask

def create_app(test_config=None):
    #
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # default value during the development
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'main.sqlite'),
    )
    if test_config is None:
        # Here the secret_key gets overridden
        app.config.from_pyfile('config.py', silent=True)
    else:
        #
        app.config.from_mapping(test_config)

    #
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #
    @app.route('/hello')
    def hello():
        return 'Hello, world!'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app