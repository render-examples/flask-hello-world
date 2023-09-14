import json
from flask import Flask,request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def save_to_json():
    with open('responses.json', 'w') as file:
        json.dump(responses, file)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    responses.append(data)
    save_to_json()
    return jsonify(success=True), 200

@app.route('/get_responses', methods=['GET'])
def get_responses():
    with open('responses.json', 'r') as file:
        data = json.load(file)
    return jsonify(data), 200


