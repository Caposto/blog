from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import configuration modules
from instance.config import DevelopmentConfig

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DevelopmentConfig)

# Initialize Database
db = SQLAlchemy(app)

# Welcome Page
@app.route('/')
def index():
    return render_template("index.html")

# Class representing a blog post
class BlogPost(db.Model):
    title = db.Column(db.String(50), primary_key=True)
    body = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog Post %r>' % self.title

# Routes user to the blog page
# is url_for() method better?
@app.route('/blog', methods=['POST', 'GET'])
def blog_index():
    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        new_post = BlogPost(title=post_title, body=post_body)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        except:
            return "There was an error uploading your post"
    else:
        blog_posts = BlogPost.query.order_by(BlogPost.date_created).all()
        return render_template("blog.html", blog_posts=blog_posts)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
