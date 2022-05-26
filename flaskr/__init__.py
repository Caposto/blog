from wsgiref import headers
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ
from dotenv import load_dotenv
import json
import requests

load_dotenv()

# Import configuration modules
from flaskr.config import DevelopmentConfig

# Create and Configure App
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DevelopmentConfig)

# Initialize Sqlite Database 
db = SQLAlchemy(app)

# Notion API
notion_token = environ.get("NOTION_API_SECRET_KEY")
notion_database_id = environ.get("NOTION_DATABASE_ID")

headers = {
    "Authorization": "Bearer " + notion_token,
    "Notion-Version": "2022-02-22"
}

@app.before_first_request
def create_tables():
    db.create_all()

# Welcome Page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/notion')
def read_database():
    read_url = f"https://api.notion.com/v1/databases/{notion_database_id}/query"

    result = requests.request("POST", read_url, headers=headers)

    status = result.status_code
    text = result.text
    json_load = (json.loads(text))
    url = json_load['results'][0]['properties']['Content Link']['url']
    title = json_load['results'][0]['properties']['Title']['title'][0]['text']['content']
    page_status = json_load['results'][0]['properties']['Status']['select']['name']
    page_id = json_load['results'][0]['id'] 

    pg_url = f"https://api.notion.com/v1/pages/{page_id}"
    pg_result = requests.request("GET", pg_url, headers=headers)
    pg_text = pg_result.text
    # Add try block

    return render_template("notion.html", status=status, title=title, url=url, page_status=page_status, pg_text=pg_text, json_load=json_load)

@app.route('/notion_post/<string:title>')
def show_post():
    read_url = f"https://api.notion.com/v1/blocks/{block_id}/children"

    result = requests.request("GET", read_url, headers=headers)
    return result

# Class representation of a blog post
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content_link = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)

    def __init__(self, title, content, date_posted=datetime.now()):
        self.title = title
        self.content = content
        self.date_posted = date_posted
    

# Routes user to the blog page which shows all the current blog posts in the database
@app.route('/blog')
def blog_index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template("blog.html", posts=posts)

# Add a new blog post to blog.db using information from html form in blog.html
@app.route('/add_post', methods=["POST"])
def add_post():
    title = request.form['title']
    content = request.form['body']

    new_post = Blogpost(title, content)

    try:
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog_index'))
    except:
        return "There was an error adding your post!"

# Deletes blog post from blog.db based on the post's ID
@app.route('/delete_post/<int:id>')
def delete_post(id):
    post_to_delete = Blogpost.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect(url_for('blog_index'))
    except:
        return "There was an error deleting your post!"

# Edits a post in blog.db based on the post's ID and information in form in update.html
@app.route('/edit_post/<int:id>', methods = ["GET", "POST"])
def edit_post(id):
    post_to_edit = Blogpost.query.get_or_404(id)

    if request.method == 'POST':
        post_to_edit.content = request.form['body']

        try:
            db.session.commit()
            return redirect(url_for('blog_index'))
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', post=post_to_edit)

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
