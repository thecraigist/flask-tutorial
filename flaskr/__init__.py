import os

from flask import Flask


# C:\Users\clewi\Desktop\FFL\Pycharm\flaskProject\venv\Scripts>activate
# cd C:\Users\clewi\Desktop\FFL\Pycharm\flaskProject>
# set FLASK_APP=flaskr
# set FLASK_ENV=development
# flask run
# if css not responding, hard refresh ctrl+shift+r


# TODO commit to GIT as version1.0, continue below
# TODO reply to a message (nested)
# TODO add in charts and other things (https://www.jetbrains.com/help/pycharm/creating-web-application-with-flask.html)
# TODO start new project specific to fantasy football; use matplotlib like in above example
# TODO host on heroku? pythonanywhere?; use signals (pubsub) to notify league members when updated
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
