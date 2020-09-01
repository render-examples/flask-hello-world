from flask import Flask, render_template
import requests
import requests_cache
import mistune
from dateutil.parser import parse
import os
import config

app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)


requests_cache.install_cache('trello_cache', backend='sqlite', expire_after=300)

markdown = mistune.Markdown()

def all_content_ids(content_type):
    """ get short ids of all active content """
    if content_type == "post":
        content = config.POSTS_LABEL
    elif content_type == "page":
        content = config.PAGES_LABEL
    elif content_type == "download":
        content = config.DOWNLOADS_LABEL
    elif content_type == "link":
        content = config.LINKS_LABEL
    payload = {
        'key': config.TRELLO_KEY,
        'token': config.TRELLO_TOKEN,
        }
    url = "https://api.trello.com/1/boards/" + config.BOARD_ID + "/cards/open"
    r = requests.get(url, params=payload)
    cards = r.json()
    items = []
    for card in cards:
        labels = card["idLabels"]
        if content in labels:
            if card["dueComplete"] == True:
                item_id = card["shortLink"]
                items.append(item_id)
    return items

def create_loop(content_type):
    """ make a loop for any of the content types """
    payload = {
        'key': config.TRELLO_KEY,
        'token': config.TRELLO_TOKEN,
        }
    items = all_content_ids(content_type)
    item_loop = []
    for item_id in items:
        # content
        content_url = "https://api.trello.com/1/cards/" + item_id
        content_r = requests.get(content_url, params=payload)
        content = content_r.json()
        dt = parse(content.get("due", "NA"))
        date = dt.date()
        image = None
        if content_type == "post":
            # attachments
            payload = {
                'key': config.TRELLO_KEY,
                'token': config.TRELLO_TOKEN,
                'filter': 'cover'
                }
            attachments_url = "https://api.trello.com/1/cards/" + item_id + "/attachments"
            attachments_r = requests.get(attachments_url, params=payload)
            attachments = attachments_r.json()
            image = attachments[0]["url"]
        info = {
                "date": date,
                "item_id": item_id,
                "title": content.get("name", "NA"),
                "image": image,
                "text": content.get("desc", "NA"),
            }
        item_loop.append(info)
    return item_loop

def get_all_cards():
    """ for debugging """
    payload = {
        'key': config.TRELLO_KEY,
        'token': config.TRELLO_TOKEN,
        }
    url = "https://api.trello.com/1/boards/" + config.BOARD_ID + "/cards/open"
    r = requests.get(url, params=payload)
    return r.json()


@app.route("/")
def index():
    post_loop = create_loop("post")
    page_loop = create_loop("page")
    download_loop = create_loop("download")
    link_loop = create_loop("link")
    return render_template("index.html", post_loop=post_loop, page_loop=page_loop,
        download_loop=download_loop, link_loop=link_loop)

@app.route("/post/<post_id>")
def post(post_id):
    payload = {
        'key': config.TRELLO_KEY,
        'token': config.TRELLO_TOKEN,
        }
    # content
    content_url = "https://api.trello.com/1/cards/" + post_id
    content_r = requests.get(content_url, params=payload)
    content = content_r.json()
    text = markdown(content.get("desc", "NA"))
    dt = parse(content.get("due", "NA"))
    date_text = dt.date().strftime("%-d %B %Y")
    # attachments
    attachments_url = "https://api.trello.com/1/cards/" + post_id + "/attachments"
    attachments_r = requests.get(attachments_url, params=payload)
    attachments = attachments_r.json()
    # meta
    meta_url = "https://api.trello.com/1/cards/" + post_id + "/customFieldItems"
    meta_r = requests.get(meta_url, params=payload)
    meta = meta_r.json()
    page_loop = create_loop("page")
    post_loop = create_loop("post")
    link_loop = create_loop("link")
    download_loop = create_loop("download")
    return render_template("post.html", page_loop=page_loop, content=content,
        attachments=attachments, meta=meta, text=text, date_text=date_text,
        link_loop=link_loop, post_loop=post_loop, download_loop=download_loop,
        post_id=post_id)

@app.route("/page/<page_id>")
def page(page_id):
    payload = {
        'key': config.TRELLO_KEY,
        'token': config.TRELLO_TOKEN,
        }
    # content
    content_url = "https://api.trello.com/1/cards/" + page_id
    content_r = requests.get(content_url, params=payload)
    content = content_r.json()
    text = markdown(content.get("desc", "NA"))
    dt = parse(content.get("due", "NA"))
    date_text = dt.date().strftime("%d %B %Y")
    page_loop = create_loop("page")
    post_loop = create_loop("post")
    link_loop = create_loop("link")
    download_loop = create_loop("download")
    return render_template("page.html", content=content, text=text,
        date_text=date_text, link_loop=link_loop, post_loop=post_loop, page_loop=page_loop,
        download_loop=download_loop, page_id=page_id)

@app.route("/download/<download_id>")
def download(download_id):
    payload = {
        'key': config.TRELLO_KEY,
        'token': config.TRELLO_TOKEN,
        }
    # content
    content_url = "https://api.trello.com/1/cards/" + download_id
    content_r = requests.get(content_url, params=payload)
    content = content_r.json()
    text = markdown(content.get("desc", "NA"))
    dt = parse(content.get("due", "NA"))
    date_text = dt.date().strftime("%d %B %Y")
    download_loop = create_loop("download")
    page_loop = create_loop("page")
    post_loop = create_loop("post")
    link_loop = create_loop("link")
    return render_template("page.html", content=content, text=text,
        date_text=date_text, link_loop=link_loop, post_loop=post_loop, page_loop=page_loop,
        download_loop=download_loop, download_id=download_id)
