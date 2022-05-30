import requests
import json
# Module that handles all requests to the Notion API

def get_database(notion_database_id, headers):
    read_url = f"https://api.notion.com/v1/databases/{notion_database_id}/query"
    result = requests.request("POST", read_url, headers=headers)
    status = result.status_code

    if status == 200:
        return result.text
    else:
        return "Error accessing database!"

def get_page(page_id, headers):
    read_url = f"https://api.notion.com/v1/pages/{page_id}"
    result = requests.request("GET", read_url, headers=headers)
    status = result.status_code

    if status == 200:
        return result.text
    else:
        return "Error accessing page!"

def get_blocks(page_id, headers):
    read_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    result = requests.request("GET", read_url, headers=headers)
    status = result.status_code

    if status == 200:
        return json.loads(result.text)
    else:
        return "Error accessing blocks!"