from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return {'test' : 'app'}

@app.route('/testing')
def testing():
    return {"WOAH" : "this route works"}