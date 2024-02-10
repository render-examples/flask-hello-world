from flask import Flask, render_template, redirect
from flask import jsonify
from flask import request
import tkinter as tk
from flask_cors import CORS
import random
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return render_template("home.html", my_rec=my_recordings)

if __name__ == "__main__":
    app.run()

#
# @app.route('/create-lesson')
# def create_lesson():
#     name = request.args["name"]
#     credits = request.args["credits"]
#     id = len(lessons) + 1
#     newLesson = {"id": id, "name": name, "credits": credits}
#     lessons.append(newLesson)
#     return jsonify(lessons)
#
# @app.route('/delete/<lesson_id>', methods=["GET"])
# def delete_lesson(lesson_id):
#     for lesson in lessons:
#         if lesson["id"] == int(lesson_id):
#             lessons.remove(lesson)
#     # return jsonify(lessons)
#     return redirect("/lessons-jinja")
#

my_recordings = {}

@app.route('/saveRecording', methods=["POST"])
def saveRecording():
    data = request.get_json()
    print(data)
    return {"status" : "OK"}



# SAVE, DELETE, SHOW