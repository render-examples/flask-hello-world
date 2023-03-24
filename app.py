from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Render!'

@app.route('/bad')
def good_bye_world():
    return "Page nut found", 404
