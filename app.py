from flask import Flask, request, jsonify
from autosuggest import get_autosuggest

app = Flask(__name__)

@app.route('/get_autosuggest', methods=['GET'])
def autosuggest():
    query = request.args.get('query')
    suggestions = get_autosuggest(query)
    return jsonify(suggestions=suggestions)

if __name__ == '__main__':
    app.run()
