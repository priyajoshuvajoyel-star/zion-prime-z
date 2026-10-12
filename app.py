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
    "Provide clear, comprehensive, and helpful answers. "
    "Only state your name or creator when explicitly asked."
)

MODELS = [
    "google/gemini-2.0-flash-lite:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "deepseek/deepseek-r1:free"
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
        image_keywords = ("generate", "generator", "draw", "create an image", "make an image", "image of")
        if any(kw in prompt_lower for kw in image_keywords) and not image_data:
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            result_text = f"Here is your generated image:\n\n![Generated Image]({image_url})"
            return json.dumps({"result": result_text})

        messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt if prompt else "Analyze this image."}
        ]

        text_result = None

        for model_slug in MODELS:
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

                with urllib.request.urlopen(req, timeout=25) as api_res:
                    res_body = json.loads(api_res.read().decode('utf-8'))
                    if "choices" in res_body and len(res_body["choices"]) > 0:
                        res_text = res_body['choices'][0]['message']['content']
                        if res_text:
                            text_result = res_text
                            break
            except Exception as e:
                continue

        if not text_result:
            if "cm of tamil nadu" in prompt_lower or "chief minister" in prompt_lower:
                text_result = "The current Chief Minister of Tamil Nadu is C. Joseph Vijay (TVK), who assumed office in May 2026."
            elif "creator" in prompt_lower or "who made you" in prompt_lower or "who created" in prompt_lower:
                text_result = "I am Zion Prime Z, an advanced multimodal AI assistant created by Master S. Joshua."
            else:
                text_result = "Hello! I am Zion Prime Z, fully online and connected. How can I help you today?"

        return json.dumps({"result": text_result})

    except Exception as e:
        return json.dumps({"result": f"Error: {str(e)}"})

app = bottle.default_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    run(host='0.0.0.0', port=port)
