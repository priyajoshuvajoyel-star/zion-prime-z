import os
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
        # Pull message from JSON, form, or raw body safely
        user_message = ""
        if request.is_json:
            data = request.get_json(silent=True) or {}
            user_message = data.get("message", "") or data.get("prompt", "")
        
        if not user_message and request.form:
            user_message = request.form.get("message", "")

        if not user_message:
            user_message = request.data.decode('utf-8', errors='ignore').strip()

        if not user_message:
            user_message = "Hello from Zion Prime Z"

        # Direct response matching your app expectations
        return jsonify({
            "response": f"Zion Prime Z active. Received your message: {user_message}"
        })

    except Exception as err:
        return jsonify({"response": f"Error: {str(err)}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
