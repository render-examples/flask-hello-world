from flask import Flask, render_template, redirect, jsonify, request
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

db = SQLAlchemy()

@app.route('/')
def hello_world():
    return render_template("home.html", my_rec=recordings)

if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://robert:LTrCCDwSsyrNhFKffv5TewRi1TQXX9Hs@dpg-cn3qur5jm4es73bmkga0-a.frankfurt-postgres.render.com/recordingsdatabase'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()



# SAVE, DELETE, SHOW

# Database integration

class Recording(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data = db.Column(db.Text)  # This stores JSON data as text

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "data": self.data
        }

def jsonify_recordings(recordings):
    result = []
    for recording in recordings:
        result.append({
            "id": recording.id,
            "name": recording.name,
            # "description": recording.description
        })
    return result

# My recordings JS to Flask RESTful API
recordings = {}


@app.route('/saveRecording', methods=["POST"])
def saveRecording():
    data = request.get_json()  # This is your dataOfClicks from the frontend
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Assuming you want to use the name as a unique identifier for now, but you could modify this
    name = data.get('name', 'Unnamed Recording')
    recording_data = json.dumps(data.get('clicks', []))  # Convert the clicks list to a JSON string

    new_recording = Recording(name=name, data=recording_data)
    db.session.add(new_recording)
    db.session.commit()

    return jsonify({"status": "OK", "id": new_recording.id})