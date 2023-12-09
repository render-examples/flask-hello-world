from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    """
    API Endpoint: /
    HTTP Method: GET

    Get a simple "Hello, World!" message.

    Request:
    - Method: GET

    Response:
    - Success (HTTP 200 OK):
        {
            "message": "Hello, World!"
        }
    """
    data = {"message": "Hello, World!"}
    return jsonify(data), 200


@app.route("/api/v1/submit", methods=["POST"])
def submit():
    """
    API Endpoint: /api/v1/submit
    HTTP Method: POST

    Submit daily tasks data.

    Request:
    - Method: POST
    - Headers:
        Content-Type: application/json
    - Body (JSON):
        {
            "daily": [
                {"task": "cleaning", "status": true},
                {"task": "exercise", "status": false},
                ...
            ]
        }

    Response:
    - Success (HTTP 200 OK):
        {
            "message": "Data received successfully"
        }
    - Bad Request (HTTP 400 Bad Request):
        {
            "error": "Invalid data format"
        }
    - Internal Server Error (HTTP 500 Internal Server Error):
        {
            "error": "Unexpected error occurred"
        }
    """
    try:
        # POSTリクエストのボディからJSONデータを取得
        json_data = request.get_json()

        # "daily" キーが存在し、その値がリストであることを確認
        if "daily" in json_data and isinstance(json_data["daily"], list):
            daily_data = json_data["daily"]

            # daily_dataを処理する (ここでは単に表示する例)
            for item in daily_data:
                task = item.get("task")
                status = item.get("status")
                print(f"Task: {task}, Status: {status}")

            # 応答として成功メッセージを返す
            return jsonify({"message": "Data received successfully"}), 200

        else:
            # 必要なデータが見つからない場合はエラーメッセージを返す
            return jsonify({"error": "Invalid data format"}), 400

    except Exception as e:
        # 例外が発生した場合はエラーメッセージを返す
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/points")
def get_points():
    """
    API Endpoint: /api/v1/points
    HTTP Method: GET

    Get the user's points.

    Request:
    - Method: GET

    Response:
    - Success (HTTP 200 OK):
        {
            "points": 88
        }
    """
    data = {"points": 88}
    return jsonify(data), 200


if __name__ == "__main__":
    app.run()
