from wsgiref import headers
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
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
cache = Cache(app)

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
@cache.cached(timeout=30)
def read_database():
    read_url = f"https://api.notion.com/v1/databases/{notion_database_id}/query"

    result = requests.request("POST", read_url, headers=headers)
    status = result.status_code

    if status == 200:
        text = result.text
        posts_json = (json.loads(text))
        posts = []

        for post_json in posts_json['results']:
            post_info = {}
            
            url = post_json['properties']['Content Link']['url']
            title = post_json['properties']['Title']['title'][0]['text']['content']
            post_status = post_json['properties']['Status']['select']['name']

            post_info['url'] = url
            post_info['Title'] = title
            post_info['Status'] = post_status

            posts.append(post_info)

        return render_template("notion.html", posts=posts)

    else:
        return "The blog is currently unavailable, please come back soon!"

class Notionpost(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(200))
    url = db.Column(db.String(200))
    status = db.Column(db.Boolean)
    date_posted = db.Column(db.String(200))

    def __init__(self, title, url, status, date_posted):
        self.title = title
        self.url = url
        self.status = status
        self.date_posted = date_posted

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
