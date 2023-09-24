from flask import Flask, request
app = Flask(__name__)

import json

from flask_cors import CORS

from flask import Response

from models import llm
from models import txtmodel
from models import jsonloader
from models import expfind


CORS(app)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/ask", methods=["POST"])
def ask():
    question = request.get_json()
    return (txtmodel.txtmodel.get_response(question['query']))


@app.route("/llm", methods=["POST"])
def llm_route():
    requete = request.get_json()
    print(requete['q1'])
    print(requete['url'])
    #text = request.json["text"]
    result = llm.Llm.callLlm(requete['q1'],requete['url'])
    resp = Response(result)
    resp.charset = "utf-8"
    return resp

@app.route("/expert",  methods=["POST"])
def loadjson():
    requete = request.get_json()
    results = expfind.ExpFind.findExp(requete['message'])
    return results
