import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")
COMET_KEY = os.environ.get("COMET_API_KEY")

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST', 'GET', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        user_data = request.get_json(force=True, silent=True) or {}
        user_message = user_data.get("message", "")

        if not user_message:
            return jsonify({"response": "System operational. Please enter a prompt."})

        # Hardcoded anchors to verify immediate response
        msg_lower = user_message.lower()
        if "who are you" in msg_lower:
            return jsonify({"response": "I am Zion Prime Z, created by Master S. Joshua."})
        elif "who is the us president" in msg_lower:
            return jsonify({"response": "Donald Trump"})
        elif "who is the tn cm" in msg_lower:
            return jsonify({"response": "C. Joseph Vijay (TVK)"})

        # Attempt OpenRouter / OpenAI fallback
        prompt_payload = {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": user_message}]}
        
        if OPENROUTER_KEY:
            try:
                res = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"},
                    json=prompt_payload,
                    timeout=15
                )
                if res.status_code == 200:
                    data = res.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        return jsonify({"response": data['choices'][0]['message']['content']})
            except Exception as e:
                pass

        if OPENAI_KEY:
            try:
                res = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
                    json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": user_message}]},
                    timeout=15
                )
                if res.status_code == 200:
                    data = res.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        return jsonify({"response": data['choices'][0]['message']['content']})
            except Exception as e:
                pass

        return jsonify({"response": "Zion Prime Z fallback active: Server is online, but external API keys returned errors or rate limits."})

    except Exception as err:
        return jsonify({"response": f"Server processing error: {str(err)}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
