from __future__ import annotations
from wsgiref import headers
from flask import Flask, render_template
from flask_caching import Cache
from os import environ
from dotenv import load_dotenv
from flaskr.notion import get_database, get_page, get_blocks
from flask_cors import CORS, cross_origin
import json

load_dotenv()

# Import configuration modules
from flaskr.config import DevelopmentConfig

# Create and Configure App
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DevelopmentConfig)
cache = Cache(app)
cor = CORS(app)

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
            url = post_json['properties']['URL']['url']
            title = post_json['properties']['Title']['title'][0]['text']['content']
            category = post_json['properties']['Category']['select']['name']
            page_id = post_json['id']
            description = post_json['properties']['Description']['rich_text'][0]['text']['content']

            post_info['status'] = post_status
            post_info['url'] = url
            post_info['title'] = title
            post_info['category'] = category
            post_info['description'] = description
            post_info['id'] = page_id

            #Easy way to create a json with the required data
            #page_data = get_blocks(page_id, headers)
            #j_data = page_data.json()            
            #with open('./child.json', 'w', encoding='utf8') as f:
            #    json.dump(j_data, f, ensure_ascii=False)

            posts.append(post_info)
    return render_template("blog.html", posts=posts)

@app.route('/blog/<id>')
def render_page(id):
    block_properties = get_blocks(id, headers)
    rich_text = block_properties["results"][0]["paragraph"]["rich_text"]
    text_arr = []
    for r in rich_text:
        content = r['text']['content']
        annotations = r["annotations"]
        text_obj = Text(content, annotations['bold'], annotations['italic'], 
                        annotations['strikethrough'], annotations['underline'], 
                        annotations['code'], annotations['color'])
        text_arr.append(text_obj.get_text_props())
    
    # for block in page_properties: get_block_id and pass into a dictionary block_ids where block_id: type of block (i.e "paragraph")
    # for block_id in block_ids: render_block(block_id, block_ids[block_id])
    return render_template("post.html", texts=text_arr, json=block_properties)

class Text():
    def __init__(self, content, bold, italic, strikethrough, underline, code, color="default"):
        self.content = content
        self.bold = bold
        self.italic = italic
        self.strikethrough = strikethrough
        self.underline = underline
        self.code = code
        self.color = color
    
    def __repr__(self):
        # styles = self.get_text()
        # styled_content = {'text': self.content, 'style': styles}
        return self.content + str(self.bold + self.italic + self.strikethrough + self.underline + self.code)
    
    def get_text_props(self):
        props = {'text': self.content, 'style': self.get_style()}
        return props

    # Return text + dictionary containing stylesheets
    # Class names: bold, code, italic, strikethrough, underline
    # FIXME: json returns lowercase booleans
    def get_style(self):
       styles = ""
       if True:
           " ".join((styles, "bold"))
       if self.italic:
           " ".join((styles, "italic"))
       if self.strikethrough:
           " ".join((styles, "strikethrough"))
       if self.underline:
           " ".join((styles, "underline"))
       if self.code:
           " ".join((styles, "code"))  
       else:
           return self.content  
       return styles
    

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
