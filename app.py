import os, requests, sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_ID = os.environ.get("PHONE_NUMBER_ID")
TU_NUMERO = os.environ.get("TU_NUMERO")
VERIFY_TOKEN = "UCV_FLEX_2025"

def init_db():
    conn = sqlite3.connect("data.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS pedidos
                    (id INTEGER PRIMARY KEY, cliente TEXT, tel TEXT, total REAL, estado TEXT, fecha TEXT)""")
    conn.commit()
    conn.close()
init_db()

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"].lower()
        send_whatsapp(f"Bot UCV: Recibí '{msg}'. Estoy 24/7 🚀")
    except: pass
    return "ok", 200

def send_whatsapp(text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": TU_NUMERO, "text": {"body": text}}
    requests.post(url, headers=headers, json=payload)

@app.route("/")
def home(): return jsonify({"status": "ok"})

if __name__ == "__main__": app.run(host="0.0.0.0", port=10000)
