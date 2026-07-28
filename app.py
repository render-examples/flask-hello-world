from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, SADHANA S ,24MIC0065!'
