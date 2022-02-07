from flask import Flask, redirect
app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect('success')

@app.route('/success')
def success():
    return 'this is so successful, blah blah test change'

if __name__ == '__main__':
    app.run(host="localhost", port=4000, debug=True)