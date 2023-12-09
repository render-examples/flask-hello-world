from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    data = {'message': 'Hello, World!'}
    return jsonify(data)

# GET /api/v1/points
@app.route('/api/v1/points')
def get_points():
    data = {'points': 88}
    return jsonify(data)

if __name__ == '__main__':
    app.run()
