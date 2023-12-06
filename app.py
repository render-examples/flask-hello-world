from crypt import methods
from flask import Flask, render_template, request, jsonify
import sqlite3
from SendEmail import send_email
app = Flask(__name__)

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
conn.execute('''
    CREATE TABLE IF NOT EXISTS PicturesTaken (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image BLOB,
        datePicture DATE DEFAULT (DATE('now'))
    )
''')
conn.commit()
conn.close()
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the uploaded file to the database
        image_data = file.read()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO images (image) VALUES (?)',
                       (sqlite3.Binary(image_data),))
        conn.commit()
        conn.close()
        return jsonify({'message': 'File uploaded and inserted into the database'})


@app.route('/sendEmail', methods=['GET'])
def sendEmail():
    send_email()
    return "Email sent successfully"
