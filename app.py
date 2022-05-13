from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return os.environ.get('FLASK_ENV_VAR')
