import os
urllib_parse = __import__('urllib.parse', fromlist=['quote'])
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST', 'GET', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        user_message = ""
        if request.is_json:
            data = request.get_json(silent=True) or {}
            user_message = data.get("message", "") or data.get("prompt", "")
        
        if not user_message and request.form:
            user_message = request.form.get("message", "")

        if not user_message:
            user_message = request.data.decode('utf-8', errors='ignore').strip()

        if not user_message:
            user_message = "Hello"

        msg_lower = user_message.lower()
        
        # Image generation check
        if any(keyword in msg_lower for keyword in ["image", "photo", "draw", "picture", "paint"]) and "code" not in msg_lower:
            prompt_clean = msg_lower
            for kw in ["generate", "an", "a", "of", "image", "photo", "draw", "picture", "paint", "please"]:
                prompt_clean = prompt_clean.replace(kw, "")
            prompt_clean = prompt_clean.strip()
            if not prompt_clean:
                prompt_clean = "futuristic technology"

            encoded_prompt = urllib_parse.quote(prompt_clean)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            return jsonify({
                "response": f"Generated image for: {prompt_clean}",
                "image_url": image_url
            })

        # Code generation responses for the expo
        if "code" in msg_lower or "python" in msg_lower or "html" in msg_lower or "script" in msg_lower:
            if "python" in msg_lower:
                reply = "Here is your requested Python code snippet:\n\n```python\n# Zion Prime Z Automation Script\nimport time\n\ndef run_system():\n    print('Zion Prime Z core active...')\n    time.sleep(1)\n    print('All neural pathways verified.')\n\nif __name__ == '__main__':\n    run_system()\n```"
            elif "html" in msg_lower:
                reply = "Here is your requested HTML code snippet:\n\n```html\n<!DOCTYPE html>\n<html>\n<head>\n    <title>Zion Prime Z</title>\n</head>\n<body>\n    <h1>Spatial Intelligence Active</h1>\n</body>\n</html>\n```"
            else:
                reply = "Here is the code you requested:\n\n```javascript\n// Zion Prime Z Handler\nfunction executeTask() {\n    console.log('Executing Zion Prime Z protocol...');\n}\nexecuteTask();\n```"
        elif "who are you" in msg_lower or "what is your name" in msg_lower:
            reply = "I am Zion Prime Z, an advanced AI spatial intelligence assistant created by Master S. Joshua."
        elif "who is the us president" in msg_lower:
            reply = "Donald Trump"
        elif "who is the tn cm" in msg_lower or "chief minister" in msg_lower:
            reply = "C. Joseph Vijay (TVK)"
        elif "science expo" in msg_lower or "project" in msg_lower:
            reply = "Zion Prime Z is designed to integrate real-time AI communication with dynamic backend processing for interactive science demonstrations."
        else:
            reply = f"Zion Prime Z processed your query successfully: '{user_message}'. All systems and neural pathways are fully operational."

        return jsonify({"response": reply})

    except Exception as err:
        return jsonify({"response": f"Zion Prime Z active. Received your input."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
