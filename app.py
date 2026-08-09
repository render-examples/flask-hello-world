import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# This matches the "/" route Gumroad is expecting
@app.route('/', methods=['GET','POST' 'HEAD'])
def gumroad_webhook():
    try:
        # Securely collect the incoming transaction data from Gumroad
        data = request.form.to_dict() if request.form else request.get_json(silent=True)
        
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        # Verify the seller ID matches your unique Gumroad account profile
        incoming_seller_id = data.get('seller_id')
        expected_seller_id = os.environ.get('GUMROAD_SELLER_ID')

        if expected_seller_id and incoming_seller_id != expected_seller_id:
            return jsonify({"status": "unauthorized", "message": "Invalid seller context"}), 401

        # --- Your Custom Business Pipeline Triggers Here ---
        # The data dictionary contains: customer email, product name, and sale details.
        # Render will process your automated generation tasks completely in the cloud.
        print(f"Cloud Pipeline executed successfully for purchase: {data.get('product_name')}")
        
        return jsonify({"status": "success", "message": "Cloud pipeline executed"}), 200

    except Exception as e:
        print(f"Error handling webhook: {str(e)}")
        return jsonify({"status": "error", "message": "Internal processing error"}), 500
