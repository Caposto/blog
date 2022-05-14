import os
from pickle import STACK_GLOBAL

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# To run the application
# set FLASK_APP=flaskr
# set FLASK_ENV=development
# flask run

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        STATIC_FOLDER = os.path.join('static', 'blog_photo'),
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
    @app.route('/')
    def index():
        return render_template("index.html")

    # Routes user to the blog page
    # is url_for() method better?
    @app.route('/blog')
    def blog_index():
        return render_template("blog.html")

    return app

