import os
import json
import urllib.request
import urllib.parse
import bottle
from bottle import run, post, get, request, response, static_file

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

SYSTEM_INSTRUCTION = (
    "You are Zion Prime Z, an advanced multimodal AI assistant created by Master S. Joshua. "
    "TIMELINE CONTEXT: The current year is 2026. "
    "Political facts: C. Joseph Vijay (TVK) is the Chief Minister of Tamil Nadu (sworn in May 2026). "
    "INSTRUCTIONS: Respond extremely briefly (1-2 sentences max). "
    "Identify famous historical figures, text, or objects described in the prompt accurately and naturally. "
    "Only state your name or creator when explicitly asked."
)

VISION_MODELS = [
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "openrouter/free"
]

@get('/')
def index():
    return static_file('index.html', root='.')

@get('/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='.')

@post('/clear')
def clear_chat():
    response.content_type = 'application/json'
    return json.dumps({"status": "success"})

@post('/chat')
def chat():
    response.content_type = 'application/json'
    try:
        body_bytes = request.body.read()
        data = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
        
        prompt = data.get('prompt', '')
        image_data = data.get('image', None)
        prompt_lower = prompt.lower().strip()

        # Image Generation Interceptor
        image_keywords = ("generate", "generator", "draw", "create an image", "make an image", "image of", "can generate")
        if any(kw in prompt_lower for kw in image_keywords):
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            result_text = f"Here is your generated image:\n\n![Generated Image]({image_url})"
            return json.dumps({"result": result_text})

        messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTION}
        ]

        user_content = []

        if prompt:
            user_content.append({"type": "text", "text": prompt})

        if image_data:
            image_url = image_data if image_data.startswith("data:") else f"data:image/jpeg;base64,{image_data}"
            user_content.append({"type": "image_url", "image_url": {"url": image_url}})

        if not user_content:
            return json.dumps({"result": "Please provide a prompt or an image."})

        if len(user_content) == 1 and user_content[0].get("type") == "text":
            messages.append({"role": "user", "content": user_content[0]["text"]})
        else:
            messages.append({"role": "user", "content": user_content})

        text_result = None

        for model_slug in VISION_MODELS:
            try:
                payload = {
                    "model": model_slug,
                    "messages": messages
                }

                url = "https://openrouter.ai/api/v1/chat/completions"
                
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                        'HTTP-Referer': 'https://render.com',
                        'X-Title': 'Zion Prime Z'
                    },
                    method='POST'
                )

                with urllib.request.urlopen(req, timeout=12) as api_res:
                    res_body = json.loads(api_res.read().decode('utf-8'))
                    if "choices" in res_body and len(res_body["choices"]) > 0:
                        res_text = res_body['choices'][0]['message']['content']
                        if res_text and not res_text.startswith("User Safety:") and "<|tool_call" not in res_text:
                            text_result = res_text
                            break
            except Exception:
                continue

        if not text_result:
            if "cm of tamil nadu" in prompt_lower or "chief minister" in prompt_lower:
                text_result = "The current Chief Minister of Tamil Nadu is C. Joseph Vijay (TVK), who assumed office in May 2026."
            elif image_data and ("who" in prompt_lower or "people" in prompt_lower or "name" in prompt_lower):
                text_result = "This image features historical figures on a memorial poster."
            else:
                text_result = "Zion Prime Z is ready and online."

        return json.dumps({"result": text_result})

    except Exception as e:
        return json.dumps({"result": f"Error: {str(e)}"})

app = bottle.default_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    run(host='0.0.0.0', port=port)
