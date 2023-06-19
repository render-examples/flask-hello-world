import os
import re
import logging

from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
app = Flask(__name__)

# Requires that "Less secure app access" be on
# https://support.google.com/accounts/answer/6010255
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_SERVER"] =   "mail.pylypovych.net"  # "smtp.gmail.com"
app.config["MAIL_USE_TLS"] =  True
app.config["MAIL_PORT"] =     587  #465  #587
mail = Mail(app)

MESSAGE = ""

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route("/")
def index():
    return render_template("index.html", message=MESSAGE)

@app.route("/documents")
def documents():
    return render_template("documents.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/links")
def links():
    return render_template("links.html")

@app.route("/email_sent", methods=["POST"])
def send_email():

    # Validate submission
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    subject = request.form.get("subject")
    message = request.form.get("message")

    # Send email
    body = "Name: " + name + "\n" + "Email: " + email + "\n" + "Phone: " + phone + "\n" + "Address: " + address + "\n" + "\n" + message
    message = Message(subject=subject, recipients=["mpylypov@gmail.com"], body=body)
    print(message)
    mail.send(message)
    global MESSAGE
    MESSAGE = "Thanks! Message sent."

    # Redirects to index.html
    return redirect("/", code=302)
