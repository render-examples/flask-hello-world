from crypt import methods
from flask import Flask, render_template
app = Flask(__name__)

flag = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/trigger')
def trigger_action():
    if flag:
        flag = False
        return "Action triggered!"
    else:
        return "Action not triggered!"


@app.route('/buttonPressed', methods=['GET'])
def buttonPressed_action():
    flag = True
    return render_template('index.html')
