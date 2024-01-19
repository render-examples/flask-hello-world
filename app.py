from flask import Flask
from flask import jsonify
from flask import request
import tkinter as tk
import random
app = Flask(__name__)

lessons = [
    {"id": 1, "name": "Python programing", "credits": 5},
    {"id": 2, "name": "Java programing", "credits": 4},
    {"id": 3, "name": "TypeScript programing", "credits": 3},
    {"id": 4, "name": "C++ programing", "credits": 1}
]

@app.route('/')
def hello_world():
    return 'Hello, World! Local testing'

@app.route('/lessons')
def get_lessons():
    return jsonify(lessons)

if __name__ == "__main__":
    app.run()


@app.route('/create-lesson')
def create_lesson():
    name = request.args["name"]
    credits = request.args["credits"]
    id = len(lessons) + 1
    newLesson = {"id": id, "name": name, "credits": credits}
    lessons.append(newLesson)
    return jsonify(lessons)

@app.route('/delete/<lesson_id>', methods=["GET"])
def delete_lesson(lesson_id):
    for lesson in lessons:
        if lesson["id"] == int(lesson_id):
            lessons.remove(lesson)
    return jsonify(lessons)

@app.route('/test')
def test():
    # Create the main application window
    root = tk.Tk()

    # Set the size of the window to 640x800 pixels
    root.geometry("800x640")

    # Set a title for the window
    root.title("Application Window")

    root.configure(bg="grey")

    def change_button(old_button):
        old_button.place_forget()  # This removes the old button
        create_trolled_button()

    def create_trolled_button():
        x_pos = random.randint(0, 750)
        y_pos = random.randint(0, 610)
        trolled_button = tk.Button(root, text="Get Trolled", command=lambda:
        [trolled_button.place_forget(), create_trolled_button()])
        trolled_button.pack()
        trolled_button.place(x=x_pos, y=y_pos)

    play_button = tk.Button(root, text="Play", command=lambda: change_button(play_button), fg="black", bg="white")
    play_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Run the application
    root.mainloop()
