from flask import Flask, render_template
from flask_caching import Cache
from flask_cors import CORS, cross_origin
from os import environ
from dotenv import load_dotenv
from flaskr.notion import get_database
import json

load_dotenv()

# Import configuration modules
from flaskr.config import DevelopmentConfig

# Create and Configure App
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DevelopmentConfig)
cache = Cache(app)
cors = CORS(app)

# Notion API Tokens
notion_token = environ.get("NOTION_API_SECRET_KEY")
notion_database_id = environ.get("NOTION_DATABASE_ID")
headers = {
    "Authorization": "Bearer " + notion_token,
    "Notion-Version": "2022-02-22",
    "Content-Type" : "application/json"
}

# Welcome Page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/blog')
@cache.cached(timeout=30)
@cross_origin()
def read_database():
    text = get_database(notion_database_id, headers)
    posts_json = (json.loads(text))
    posts = []

    for post_json in posts_json['results']:
        post_info = {}
        post_status = post_json['properties']['Status']['select']['name']

        if post_status == "Active":
            # Key through json to parse relative properties
            url = post_json['properties']['URL']['url']
            title = post_json['properties']['Title']['title'][0]['text']['content']
            category = post_json['properties']['Category']['select']['name']
            page_id = post_json['id']
            description = post_json['properties']['Description']['rich_text'][0]['text']['content']

            # Store Post Information in a dictionary
            post_info['status'] = post_status
            post_info['url'] = url
            post_info['title'] = title
            post_info['category'] = category
            post_info['description'] = description
            post_info['id'] = page_id

            # Add post information to the array of available posts
            posts.append(post_info)
    return render_template("blog.html", posts=posts)

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
