import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# جلب الإعدادات من متغيرات البيئة في Railway
ODOO_MCP_URL = os.environ.get("ODOO_MCP_URL")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
GREEN_API_URL = os.environ.get("GREEN_API_URL")

# رقمك الشخصي المعتمد للتفاعل مع البوت
ALLOWED_PHONE = "212663400960"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # التأكد واش الميساج جاي من الواتساب
    if data.get("typeWebhook") == "incomingMessageReceived":
        sender_data = data.get("senderData", {})
        sender_phone = sender_data.get("chatId", "").split("@")[0]

        # فلترة الرقم: إذا لم يكن رقمك، يتجاهله النظام تماماً
        if sender_phone != ALLOWED_PHONE:
            return jsonify({"status": "ignored", "reason": "Unauthorized number"}), 200

        # استخراج نص الرسالة
        message_data = data.get("messageData", {})
        text_message = message_data.get("textMessageData", {}).get("textMessage", "")

        if text_message:
            # 1. إرسال السؤال إلى Odoo MCP
            headers = {"Authorization": f"Bearer {BEARER_TOKEN}", "Content-Type": "application/json"}
            payload = {"query": text_message}

            try:
                odoo_response = requests.post(ODOO_MCP_URL, json=payload, headers=headers, timeout=30)
                answer = odoo_response.json().get("response", "عذراً، لم أتمكن من العثور على الإجابة في نظام Odoo.")
            except Exception as e:
                answer = f"حدث خطأ أثناء الاتصال بنظام Odoo: {str(e)}"

            # 2. الرد حصرياً على رقمك الشخصي عبر Green API
            payload_wa = {
                "chatId": f"{ALLOWED_PHONE}@c.us",
                "message": answer
            }
            requests.post(GREEN_API_URL, json=payload_wa)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
