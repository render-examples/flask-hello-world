from flask import Flask, request
app = Flask(__name__)

from models import txtmodel

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/ask", methods=["POST"])
def ask():
    question = request.get_json()
    return (txtmodel.txtmodel.get_response(question['query']))