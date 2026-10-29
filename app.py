import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load API keys from Render Environment Variables
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")
COMET_KEY = os.environ.get("COMET_API_KEY")

def call_llm_with_fallback(user_prompt):
    providers = []

    if OPENAI_KEY:
        providers.append({
            "name": "OpenAI",
            "url": "https://api.openai.com/v1/chat/completions",
            "headers": {"Authorization": f"Bearer {OPENAI_KEY}"},
            "payload": {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": user_prompt}]}
        })

    if OPENROUTER_KEY:
        providers.append({
            "name": "OpenRouter",
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "headers": {"Authorization": f"Bearer {OPENROUTER_KEY}"},
            "payload": {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": user_prompt}]}
        })

    if COMET_KEY:
        providers.append({
            "name": "CometAPI",
            "url": "https://api.cometapi.com/v1/chat/completions",
            "headers": {"Authorization": f"Bearer {COMET_KEY}"},
            "payload": {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": user_prompt}]}
        })

    for provider in providers:
        try:
            res = requests.post(provider["url"], headers=provider["headers"], json=provider["payload"], timeout=10)
            if res.status_code == 200:
                data = res.json()
                return data['choices'][0]['message']['content']
            else:
                print(f"[{provider['name']}] Failed with status code {res.status_code}. Trying next...")
        except Exception as e:
            print(f"[{provider['name']}] Error: {str(e)}. Trying next...")

    return "Local Fallback: Zion Prime Z core neural pathways active. External AI providers are temporarily undergoing rate limits."

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.json
    user_message = user_data.get("message", "")

    if "who are you" in user_message.lower():
        return jsonify({"response": "I am Zion Prime Z, created by Master S. Joshua."})
    elif "who is the us president" in user_message.lower():
        return jsonify({"response": "Donald Trump"})
    elif "who is the tn cm" in user_message.lower():
        return jsonify({"response": "C. Joseph Vijay (TVK)"})

    ai_reply = call_llm_with_fallback(user_message)
    return jsonify({"response": ai_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
