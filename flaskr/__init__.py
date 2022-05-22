from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import configuration modules
from instance.config import DevelopmentConfig

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DevelopmentConfig)

# Initialize Database
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Welcome Page
@app.route('/')
def index():
    return render_template("index.html")

# Class representing a blog post
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

# Routes user to the blog page
# is url_for() method better?
@app.route('/blog', methods=['POST', 'GET'])
def blog_index():
    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        new_post = Blogpost(title=post_title, body=post_body)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        except:
            return "There was an error uploading your post"
    else:
        posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
        return render_template("blog.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)
