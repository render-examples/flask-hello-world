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


@app.route("/api/v1/plans/suggest", methods=['POST'])
def suggest_plans():
    """
    API Endpoint: /api/v1/plans/suggest
    HTTP Method: POST

    Generate suggested daily plans based on the user's goal and tasks.

    Request:
    - Method: POST
    - Headers:
        Content-Type: application/json
    - Body (JSON):
        {
            "goal": "computer",
            "goal_points": 100,
            "tasks": [
                {"task": "cleaning", "award": 5},
                {"task": "wash dishes", "award": 2}
            ]
        }

    Response:
    - Success (HTTP 200 OK):
        {
            "plans": [
                {"day": 1, "plans_today": [{"task": "cleaning", "award": 5}, ...]},
                {"day": 2, "plans_today": []},
            ]
        }
    - Bad Request (HTTP 400 Bad Request):
        {
            "error": "Invalid data format"
        }
    """

    try:
        # POSTリクエストのボディからJSONデータを取得
        request_data = request.get_json()

        # 必要なデータが揃っているか確認
        if 'goal' in request_data and 'goal_points' in request_data and 'tasks' in request_data:
            goal = request_data['goal']
            goal_points = request_data['goal_points']
            tasks = request_data['tasks']

            # プランを生成するロジック (ここでは簡略化)
            plans = generate_daily_plans(goal, goal_points, tasks)

            # 生成したプランを含むレスポンスを返す
            return jsonify({"plans": plans}), 200
        else:
            # 必要なデータが見つからない場合はエラーメッセージを返す
            return jsonify({"error": "Invalid data format"}), 400

    except Exception as e:
        # 例外が発生した場合はエラーメッセージを返す
        return jsonify({"error": str(e)}), 500

def generate_daily_plans(goal, goal_points, tasks):
    # TODO: プラン生成のロジックを追加する
    day1_plan = {"day": 1, "plans_today": [task for task in tasks]}
    day2_plan = {"day": 2, "plans_today": []}
    plans = [day1_plan, day2_plan]

    return plans


@app.route("/api/v1/plans/accept")
def accept_plan():
    """
    API Endpoint: /api/v1/plans/accept
    HTTP Method: GET

    Accept the plan.

    Request:
    - Method: GET

    Response:
    - Success (HTTP 200 OK):
        {
            "message": "Plan accepted"
        }
    """
    data = {"message": "Plan accepted"}
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
