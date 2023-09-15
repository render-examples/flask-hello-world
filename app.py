import json
from flask import Flask,request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

responses = []

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def save_to_json():
    with open('responses.json', 'w') as file:
        json.dump(responses, file)

@app.route('/webhook', methods=['POST'])
def webhook():
    message_body = request.form.get('Body')
    responses.append(message_body)
    save_to_json()

    # Start our TwiML response
    resp = MessagingResponse()
        if message_body == 1 or message_body == 2:
            resp.message("Got it!")    
        else: 
            resp.message("Please send 1 or 2. I was unable to record your message.") 
    
    return str(resp)

@app.route('/get_responses', methods=['GET'])
def get_responses():
    with open('responses.json', 'r') as file:
        data = json.load(file)
    return jsonify(data), 200


