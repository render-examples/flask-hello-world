from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello from PaaS lab!Student:My name is SADHANA S, My register number is 24MIC0065"
