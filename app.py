import json
from flask import Flask,request, jsonify
import os
from twilio.twiml.messaging_response import MessagingResponse

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
TARGET_PHONE_NUMBER = os.environ.get('TARGET_PHONE_NUMBER')
JIM_PHONE_NUMBER = os.environ.get('JIM_PHONE_NUMBER')

from twilio.rest import Client


responses = []

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/webhook', methods=['POST'])
def webhook():
    message_body = request.form.get('Body')
    responses.append(message_body)

    # Start our TwiML response
    resp = MessagingResponse()
    if message_body == "1" or message_body == "2":
        resp.message("Got it!") 
        send_sms(message_body)   
    else: 
        resp.message("Please send 1 or 2. I was unable to record your message.") 
    
    return str(resp)

def send_sms(message_body):
    client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body="Got a response from James: " + message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=JIM_PHONE_NUMBER
    )
    print(f"SMS sent to dad with message ID: {message.sid}")


