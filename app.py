from flask import Flask, request
from chatai import AI_Response

app = Flask(__name__)

@app.route("/api", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        data = request.args.get("prompt")
    elif request.method == "POST":
        jsondata = request.get_json()
        data = jsondata["prompt"]

    response = AI_Response(data)
    return response

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run()