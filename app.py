from flask import Flask, render_template
app = Flask(__name__)

flag = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/trigger', methods=['GET'])
def trigger_action():
    # Code to perform the action when the button is pressed
    # This could involve sending a signal to the ESP32
    print("Button pressed!")
    # Add code to communicate with the ESP32 here
    if not flag:
        return "Action not triggered!"
    else:
        flag = True
        return "Action triggered!"


@app.route('/buttonPressed')
def buttonPressedAction():
    flag = True
    return render_template('index.html')
