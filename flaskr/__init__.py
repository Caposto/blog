from __future__ import annotations
from wsgiref import headers
from flask import Flask, render_template
from flask_caching import Cache
from os import environ
from dotenv import load_dotenv
from flaskr.notion import get_database, get_page, get_blocks
import json
import requests

load_dotenv()

# Import configuration modules
from flaskr.config import DevelopmentConfig

# Create and Configure App
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DevelopmentConfig)
cache = Cache(app)

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
def read_database():
    #read_url = f"https://api.notion.com/v1/databases/{notion_database_id}/query"
    #result = requests.request("POST", read_url, headers=headers)
    #status = result.status_code

    
    # if status == 200:
        #text = result.text
    text = get_database(notion_database_id, headers)
    posts_json = (json.loads(text))
    posts = []

    for post_json in posts_json['results']:
        post_info = {}
        post_status = post_json['properties']['Status']['select']['name']

        if post_status == "Active":
            url = post_json['properties']['URL']['url']
            title = post_json['properties']['Title']['title'][0]['text']['content']
            category = post_json['properties']['Category']['select']['name']
            page_id = post_json['id']

            post_info['status'] = post_status
            post_info['url'] = url
            post_info['title'] = title
            post_info['category'] = category
            post_info['id'] = page_id
            
            #Easy way to create a json with the required data
            #page_data = get_blocks(page_id, headers)
            #j_data = page_data.json()            
            #with open('./child.json', 'w', encoding='utf8') as f:
            #    json.dump(j_data, f, ensure_ascii=False)

            posts.append(post_info)
    return render_template("blog.html", posts=posts)
    #else:
    #    return "The blog is currently unavailable, please come back soon!"

@app.route('/blog/<id>')
def render_page(id):
    block_properties = get_blocks(id, headers)
    rich_text = block_properties['results'][0]["paragraph"]["rich_text"]

    text_arr = []
    for r in rich_text:
        text_arr.append(r["plain_text"])
    
    # for block in page_properties: get_block_id and pass into a dictionary block_ids where block_id: type of block (i.e "paragraph")
    # for block_id in block_ids: render_block(block_id, block_ids[block_id])
    return " ".join(text_arr)

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
