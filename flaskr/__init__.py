from asyncio import tasks
import os
from pickle import STACK_GLOBAL

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# To run the application
# set FLASK_APP=flaskr
# set FLASK_ENV=development
# flask run

app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
)

# Setup Database with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
db.create_all()
# a simple page that says hello
@app.route('/')
def index():
    return render_template("index.html")

# Routes user to the blog page
# is url_for() method better?
@app.route('/blog', methods=['POST', 'GET'])
def blog_index():
    if request.method == 'POST':
        post_body = request.form['body']
        new_post = Post(body=post_body)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        except:
            return "There was an error uploading your post"
    else:
        posts = Post.query.order_by(Post.date_created).all()
        return render_template("blog.html", posts=posts)

# Class representing a blog post
class Post(db.Model):
    title = db.Column(db.String(50), primary_key=True)
    body = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r' % self.id

if __name__ == "__main__":
    app.run(debug=True)
