import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST', 'GET', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        # Extract user message safely no matter how the frontend sends it
        user_message = ""
        if request.is_json:
            data = request.get_json(silent=True) or {}
            user_message = data.get("message", "") or data.get("prompt", "")
        else:
            user_message = request.form.get("message", "") or request.args.get("message", "")

        if not user_message:
            # Fallback to check raw data or body if empty
            raw_data = request.data.decode('utf-8', errors='ignore')
            if raw_data:
                user_message = raw_data
            else:
                user_message = "Hello"

        msg_lower = user_message.lower()
        if "who are you" in msg_lower:
            return jsonify({"response": "I am Zion Prime Z, created by Master S. Joshua."})
        elif "who is the us president" in msg_lower:
            return jsonify({"response": "Donald Trump"})
        elif "who is the tn cm" in msg_lower:
            return jsonify({"response": "C. Joseph Vijay (TVK)"})

        return jsonify({"response": f"Zion Prime Z received: {user_message}"})

    except Exception as err:
        return jsonify({"response": f"Server error: {str(err)}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
