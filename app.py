from flask import Flask, request
app = Flask(__name__)


from flask import Response

from models import llm
from models import txtmodel
from models import prediction

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/ask", methods=["POST"])
def ask():
    question = request.get_json()
    return (txtmodel.txtmodel.get_response(question['query']))


@app.route("/llm", methods=["POST"])
def index():
    requete = request.get_json()
    print(requete['q1'])
    print(requete['url'])
    #text = request.json["text"]
    result = llm.Llm.callLlm(requete['q1'],requete['url'])
    resp = Response(result)
    resp.charset = "utf-8"
    return resp


@app.route("/prediction", methods=["POST"])
def prediction():
    question = request.get_json()
    result = prediction.Prediction.callPrediction(question['q2'])
    resp = Response(result)
    resp.charset = "utf-8"
    return resp
