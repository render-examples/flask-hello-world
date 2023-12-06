from crypt import methods
from flask import Flask, render_template, request, jsonify
import sqlite3
import base64
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

temperature_value = 0.0


@app.route('/')
def index():
    return render_template('index.html', value=temperature_value)


@app.route('/update', methods=['POST'])
def update():
    global temperature_value

    try:
        # Extract float value from the request
        new_value = float(request.form['value'])
        print(f'Received value: {new_value}')

        # Update the current value
        temperature_value = new_value

        return 'OK', 200
    except Exception as e:
        print(f'Error: {e}')
        return 'Error', 500


@app.route('/get_value')
def get_value():
    global temperature_value
    return str(temperature_value)


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


@app.route('/gallery')
def image_gallery():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM images')
    images = cursor.fetchall()
    conn.close()

    # Convert binary image data to base64 for display in HTML
    for i, (image_id, image_data, image_date) in enumerate(images):
        images[i] = (image_id, base64.b64encode(
            image_data).decode('utf-8'), image_date)

    return render_template('gallery.html', images=images)
