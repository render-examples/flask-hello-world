from crypt import methods
from flask import Flask, render_template, request

app = Flask(__name__)

flag = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/trigger')
def trigger_action():
    global flag
    if flag:
        flag = False
        return "Action triggered!"
    else:
        return "Action not triggered!"


@app.route('/buttonPressed', methods=['GET'])
def buttonPressed_action():
    global flag
    flag = True
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Access the uploaded file using request.files
    uploaded_file = request.files['file']

    # Save the file to a desired location
    uploaded_file.save('image.png')

    return 'File uploaded successfully!'
