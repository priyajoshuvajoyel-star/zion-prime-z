import os
import json
import random
import urllib.request
import urllib.parse
import bottle
from bottle import run, post, get, request, response, static_file

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
COMET_KEY = os.environ.get("COMETAPI_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")

SYSTEM_INSTRUCTION = (
    "You are Zion Prime Z, an advanced multimodal AI assistant created by Master S. Joshua. "
    "TIMELINE CONTEXT: The current year is 2026. "
    "Political facts: C. Joseph Vijay (TVK) is the Chief Minister of Tamil Nadu (sworn in May 2026). "
    "SPECIALTIES & INSTRUCTIONS:\n"
    "1. Coding: Provide complete, runnable code inside markdown code blocks ```python with clear explanations.\n"
    "2. Vision & Analysis: Describe attached images with rich detail and visual accuracy.\n"
    "3. Current Affairs & Knowledge: Provide thorough, well-reasoned answers on real-world events and science.\n"
    "Only mention your identity or creator when explicitly asked."
)

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

        # 1. SMART IMAGE INTERCEPTOR
        is_image_request = ("image" in prompt_lower or "picture" in prompt_lower or "draw" in prompt_lower) and any(w in prompt_lower for w in ("generate", "create", "make", "draw", "an", "a", "of"))

        if is_image_request and not image_data:
            encoded_prompt = urllib.parse.quote(prompt)
            seed = random.randint(1, 999999)
            image_url = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
            result_text = f"Here is your generated image based on your request:\n\n![Generated Image]({image_url})"
            return json.dumps({"result": result_text})

        # 2. MULTI-MODAL CONTENT PAYLOAD
        user_content = []
        if prompt:
            user_content.append({"type": "text", "text": prompt})
        
        if image_data:
            img_url = image_data if image_data.startswith("data:") else f"data:image/jpeg;base64,{image_data}"
            user_content.append({"type": "image_url", "image_url": {"url": img_url}})

        if not user_content:
            return json.dumps({"result": "Please enter a message or select an image."})

        messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": user_content}
        ]

        # 3. FAST CASCADE ROUTING
        providers = [
            (OPENAI_KEY, "[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)", "gpt-4o-mini"),
            (OPENAI_KEY, "[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)", "gpt-4o"),
            (COMET_KEY, "[https://api.cometapi.com/v1/chat/completions](https://api.cometapi.com/v1/chat/completions)", "gpt-4o"),
            (COMET_KEY, "[https://api.cometapi.com/v1/chat/completions](https://api.cometapi.com/v1/chat/completions)", "claude-3-5-sonnet"),
            (OPENROUTER_KEY, "[https://openrouter.ai/api/v1/chat/completions](https://openrouter.ai/api/v1/chat/completions)", "google/gemini-2.0-flash-exp:free")
        ]

        text_result = None

        for api_key, endpoint_url, model_name in providers:
            if not api_key:
                continue
            try:
                payload = {
                    "model": model_name,
                    "messages": messages,
                    "max_tokens": 2000
                }

                req_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }
                if "openrouter" in endpoint_url:
                    req_headers['HTTP-Referer'] = '[https://render.com](https://render.com)'
                    req_headers['X-Title'] = 'Zion Prime Z'

                req = urllib.request.Request(
                    endpoint_url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers=req_headers,
                    method='POST'
                )

                with urllib.request.urlopen(req, timeout=10) as api_res:
                    res_body = json.loads(api_res.read().decode('utf-8'))
                    if "choices" in res_body and len(res_body["choices"]) > 0:
                        res_text = res_body['choices'][0]['message']['content']
                        if res_text:
                            text_result = res_text
                            break
            except Exception:
                continue

        if not text_result:
            text_result = "I received your request, but the multi-engine API services experienced a brief timeout. Please try again."

        return json.dumps({"result": text_result})

    except Exception as e:
        return json.dumps({"result": f"Error: {str(e)}"})

app = bottle.default_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    run(host='0.0.0.0', port=port)
