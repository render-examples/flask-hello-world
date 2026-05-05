from flask import Flask, render_template_string, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json
import os

app = Flask(__name__)
# システムのセキュリティキー
app.secret_key = "KASU_NO_ATAMA_SECURE_KEY"

# --- ユーザー情報の保存先（ファイル） ---
DB_FILE = "users.json"


def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)


# --- 投稿の保存先（今回はあとで作るので、一時的な仮置き場） ---
mock_posts = []
post_id_counter = 1

# --- ログイン画面の見た目（一切変更していません！） ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ログイン - カスの頭の配布</title>
    <style>
        body { background-color: #f4f7f6; color: #333; font-family: 'Helvetica Neue', Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background-color: #ffffff; border-top: 5px solid #007bff; border-radius: 8px; padding: 40px; width: 400px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
        h2 { text-align: center; color: #333; margin-top: 0; margin-bottom: 25px; font-size: 1.5rem; }
        .input-group { margin-bottom: 20px; }
        label { display: block; font-size: 0.85rem; margin-bottom: 8px; color: #555; font-weight: bold;}
        input { width: 100%; padding: 12px; background: #fafafa; border: 1px solid #ddd; color: #333; border-radius: 4px; box-sizing: border-box; outline: none; font-size: 1rem; }
        input:focus { border-color: #007bff; box-shadow: 0 0 5px rgba(0, 123, 255, 0.2); background: #fff;}
        button { width: 100%; padding: 14px; background: #007bff; border: none; border-radius: 4px; color: #ffffff; font-size: 1rem; font-weight: bold; cursor: pointer; transition: background 0.3s; }
        button:hover { background: #0056b3; }
        .msg-area { min-height: 30px; text-align: center; margin-bottom: 15px; font-weight: bold; }
        .error { color: #dc3545; font-size: 0.9rem; }
        .success { color: #28a745; font-size: 0.9rem; }
        .footer-nav { text-align: center; margin-top: 20px; font-size: 0.9rem; color: #007bff; cursor: pointer; text-decoration: underline;}
        .footer-nav:hover { color: #0056b3; }
        #signup-area { display: none; }
    </style>
</head>
<body>
<div class="login-box">
    <div class="msg-area">
        {% if msg %}<div class="{{ msg_type }}">{{ msg }}</div>{% endif %}
    </div>
    <div id="login-area">
        <h2>ログイン</h2>
        <form method="POST">
            <input type="hidden" name="action" value="login">
            <div class="input-group">
                <label>ユーザーID</label>
                <input type="text" name="user_id" value="@" oninput="if(this.value.charAt(0) !== '@') this.value = '@' + this.value.replace(/@/g, '');" required>
            </div>
            <div class="input-group">
                <label>パスワード</label>
                <input type="password" name="password" placeholder="パスワードを入力" required>
            </div>
            <button type="submit">ログイン</button>
        </form>
        <div class="footer-nav" onclick="switchMode()">新規アカウント作成はこちら</div>
    </div>
    <div id="signup-area">
        <h2>新規アカウント作成</h2>
        <form method="POST">
            <input type="hidden" name="action" value="signup">
            <div class="input-group">
                <label>ユーザー名 (最大12文字)</label>
                <input type="text" name="username" placeholder="名前を入力" maxlength="12" required>
            </div>
            <div class="input-group">
                <label>ユーザーID (英数字のみ)</label>
                <input type="text" name="user_id" value="@" oninput="if(this.value.charAt(0) !== '@') this.value = '@' + this.value.replace(/@/g, '');" required>
            </div>
            <div class="input-group">
                <label>パスワード (8文字以上・英数字記号のみ)</label>
                <input type="password" name="password" placeholder="8文字以上のパスワード" required minlength="8">
            </div>
            <button type="submit">アカウントを作成</button>
        </form>
        <div class="footer-nav" onclick="switchMode()">既存のアカウントでログイン</div>
    </div>
</div>
<script>
    function switchMode() {
        const login = document.getElementById('login-area');
        const signup = document.getElementById('signup-area');
        if (login.style.display === 'none') {
            login.style.display = 'block'; signup.style.display = 'none';
        } else {
            login.style.display = 'none'; signup.style.display = 'block';
        }
    }
</script>
</body>
</html>
"""

# --- タイムライン画面の見た目（新機能） ---
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>タイムライン - カスの頭の配布</title>
    <style>
        body { background-color: #f4f7f6; color: #333; font-family: 'Helvetica Neue', Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background: #fff; padding: 15px 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; border-top: 5px solid #007bff; }
        .post-form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
        textarea { width: 100%; height: 80px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; resize: none; margin-bottom: 10px; box-sizing: border-box; font-family: inherit; font-size: 1rem;}
        textarea:focus { border-color: #007bff; outline: none; box-shadow: 0 0 5px rgba(0,123,255,0.2); }
        .btn { background: #007bff; color: #fff; border: none; padding: 10px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .btn:hover { background: #0056b3; }
        .post-card { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px; }
        .post-header { display: flex; align-items: center; margin-bottom: 10px; }
        /* ユーザーアイコンのスタイル */
        .icon { width: 45px; height: 45px; border-radius: 50%; background: #007bff; color: white; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 1.2rem; margin-right: 15px; }
        .post-meta { display: flex; flex-direction: column; }
        .post-meta .name { font-weight: bold; font-size: 1.1rem; }
        .post-meta .userid { font-size: 0.85rem; color: #777; }
        .post-content { margin-bottom: 15px; line-height: 1.6; font-size: 1.05rem; white-space: pre-wrap; }
        /* リアクションボタンのスタイル */
        .reactions { display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; }
        .react-btn { background: #f8f9fa; border: 1px solid #ddd; padding: 6px 12px; border-radius: 20px; cursor: pointer; display: flex; align-items: center; gap: 5px; font-size: 0.9rem; text-decoration: none; color: #555; transition: 0.2s;}
        .react-btn:hover { background: #e9ecef; color: #000; }
        .comments-section { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #eee; }
        .comment { font-size: 0.9rem; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
        .comment-form { display: flex; gap: 10px; margin-top: 10px; }
        .comment-form input { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; outline: none; }
        .comment-form input:focus { border-color: #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <!-- ヘッダー -->
        <div class="header">
            <div>ログイン中: <strong>{{ username }}</strong> <span style="font-size:0.8rem; color:#777;">({{ session['user'] }})</span></div>
            <a href="/logout" style="color: #dc3545; text-decoration: none; font-weight: bold; font-size:0.9rem;">ログアウト</a>
        </div>

        <!-- 投稿フォーム -->
        <div class="post-form">
            <form action="/add_post" method="POST">
                <textarea name="content" placeholder="今どうしてる？" required></textarea>
                <div style="text-align: right;">
                    <button type="submit" class="btn">投稿する</button>
                </div>
            </form>
        </div>

        <!-- タイムライン（投稿一覧） -->
        {% for post in posts|reverse %}
        <div class="post-card">
            <!-- アイコンと名前 -->
            <div class="post-header">
                <div class="icon">{{ post.username[0] }}</div>
                <div class="post-meta">
                    <span class="name">{{ post.username }}</span>
                    <span class="userid">{{ post.user_id }}</span>
                </div>
            </div>
            
            <!-- 投稿内容 -->
            <div class="post-content">{{ post.content }}</div>
            
            <!-- ♥️ 👍 👎 リアクション -->
            <div class="reactions">
                <a href="/react/{{ post.id }}/heart" class="react-btn">♥️ {{ post.hearts }}</a>
                <a href="/react/{{ post.id }}/like" class="react-btn">👍 {{ post.likes }}</a>
                <a href="/react/{{ post.id }}/dislike" class="react-btn">👎 {{ post.dislikes }}</a>
                <span class="react-btn" style="cursor:default;">💬 コメント {{ post.comments|length }}件</span>
            </div>

            <!-- コメント欄 -->
            <div class="comments-section">
                {% for c in post.comments %}
                    <div class="comment"><strong>{{ c.username }}</strong>: {{ c.text }}</div>
                {% endfor %}
                <form action="/add_comment/{{ post.id }}" method="POST" class="comment-form">
                    <input type="text" name="comment_text" placeholder="コメントを追加..." required>
                    <button type="submit" class="btn" style="padding: 8px 15px; font-size: 0.85rem;">送信</button>
                </form>
            </div>
        </div>
        {% endfor %}
        
        {% if not posts %}
            <p style="text-align:center; color:#777; margin-top:40px;">まだ投稿がありません。最初の投稿をしてみましょう！</p>
        {% endif %}
    </div>
</body>
</html>
"""

# --- システム（裏側の処理） ---


@app.route("/", methods=["GET", "POST"])
def auth():
    msg = ""
    msg_type = ""
    db = load_db()

    if request.method == "POST":
        action = request.form.get("action")
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        if action == "signup":
            username = request.form.get("username")
            if len(username) > 12:
                msg, msg_type = "エラー: ユーザー名が12文字を超過しています。", "error"
            elif not user_id.startswith("@"):
                msg, msg_type = "エラー: IDは「@」から始める必要があります。", "error"
            elif not re.fullmatch(r"[a-zA-Z0-9]+", user_id[1:]):
                msg, msg_type = "エラー: IDは半角英数字のみ許可されています。", "error"
            elif user_id in db:
                msg, msg_type = (
                    "エラー: そのIDは既にシステムに登録されています。",
                    "error",
                )
            elif len(password) < 8:
                msg, msg_type = "エラー: パスワードは最低8文字必要です。", "error"
            elif not re.fullmatch(r"[!-~]+", password):
                msg, msg_type = (
                    "エラー: パスワードに不適切な文字が含まれています。",
                    "error",
                )
            else:
                db[user_id] = {
                    "username": username,
                    "password": generate_password_hash(password),
                }
                save_db(db)
                msg, msg_type = (
                    "登録完了: アカウントを作成しました。ログインしてください。",
                    "success",
                )

        elif action == "login":
            user = db.get(user_id)
            if user and check_password_hash(user["password"], password):
                session["user"] = user_id
                return redirect("/dashboard")
            else:
                msg, msg_type = "エラー: IDまたはパスワードが一致しません。", "error"

    return render_template_string(HTML_TEMPLATE, msg=msg, msg_type=msg_type)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    # ログイン中のユーザー名を取得
    db = load_db()
    current_username = db.get(session["user"], {}).get("username", "Unknown")

    # タイムライン画面を表示
    return render_template_string(
        DASHBOARD_TEMPLATE, posts=mock_posts, session=session, username=current_username
    )


@app.route("/add_post", methods=["POST"])
def add_post():
    global post_id_counter
    if "user" not in session:
        return redirect("/")

    user_id = session["user"]
    db = load_db()
    username = db.get(user_id, {}).get("username", "Unknown")
    content = request.form.get("content")

    # 新しい投稿をリストに追加
    mock_posts.append(
        {
            "id": post_id_counter,
            "user_id": user_id,
            "username": username,
            "content": content,
            "hearts": 0,
            "likes": 0,
            "dislikes": 0,
            "comments": [],
        }
    )
    post_id_counter += 1
    return redirect("/dashboard")


@app.route("/react/<int:post_id>/<action>")
def react(post_id, action):
    if "user" not in session:
        return redirect("/")

    # 指定された投稿のリアクション数を増やす
    for p in mock_posts:
        if p["id"] == post_id:
            if action == "heart":
                p["hearts"] += 1
            elif action == "like":
                p["likes"] += 1
            elif action == "dislike":
                p["dislikes"] += 1
            break
    return redirect("/dashboard")


@app.route("/add_comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    if "user" not in session:
        return redirect("/")

    user_id = session["user"]
    db = load_db()
    username = db.get(user_id, {}).get("username", "Unknown")
    text = request.form.get("comment_text")

    # 指定された投稿にコメントを追加
    for p in mock_posts:
        if p["id"] == post_id:
            p["comments"].append({"username": username, "text": text})
            break
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.pop("user", None)  # ログアウト処理
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
