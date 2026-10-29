import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")
COMET_KEY = os.environ.get("COMET_API_KEY")

def call_llm_with_fallback(user_prompt):
    providers = []

    # 1. OpenRouter
    if OPENROUTER_KEY:
        providers.append({
            "name": "OpenRouter",
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "headers": {"Authorization": f"Bearer {OPENROUTER_KEY}"},
            "payload": {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": user_prompt}]}
        })

    # 2. OpenAI
    if OPENAI_KEY:
        providers.append({
            "name": "OpenAI",
            "url": "https://api.openai.com/v1/chat/completions",
            "headers": {"Authorization": f"Bearer {OPENAI_KEY}"},
            "payload": {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": user_prompt}]}
        })

    # 3. CometAPI
    if COMET_KEY:
        providers.append({
            "name": "CometAPI",
            "url": "https://api.cometapi.com/v1/chat/completions",
            "headers": {"Authorization": f"Bearer {COMET_KEY}"},
            "payload": {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": user_prompt}]}
        })

    for provider in providers:
        try:
            res = requests.post(provider["url"], headers=provider["headers"], json=provider["payload"], timeout=8)
            if res.status_code == 200:
                data = res.json()
                return data['choices'][0]['message']['content']
        except Exception as e:
            print(f"[{provider['name']}] Error: {str(e)}")

    return "Local Fallback: All external API providers are currently rate-limited or updating. Core neural pathways active."

@app.route('/chat', methods=['POST', 'GET', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        user_data = request.get_json(force=True, silent=True) or {}
        user_message = user_data.get("message", "")

        if not user_message:
            return jsonify({"response": "System operational. Please enter a prompt."})

        # Hardcoded anchors
        msg_lower = user_message.lower()
        if "who are you" in msg_lower:
            return jsonify({"response": "I am Zion Prime Z, created by Master S. Joshua."})
        elif "who is the us president" in msg_lower:
            return jsonify({"response": "Donald Trump"})
        elif "who is the tn cm" in msg_lower:
            return jsonify({"response": "C. Joseph Vijay (TVK)"})

        ai_reply = call_llm_with_fallback(user_message)
        return jsonify({"response": ai_reply})

    except Exception as err:
        return jsonify({"response": f"Server processing error: {str(err)}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
