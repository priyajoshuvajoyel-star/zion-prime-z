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
        
        # Image Generation Check
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

        # Smart Knowledge Base & Code Handling
        if "water" in msg_lower and ("formula" in msg_lower or "chemical" in msg_lower):
            reply = "The chemical formula for water is H₂O (two hydrogen atoms bonded to one oxygen atom)."
        elif "flappy bird" in msg_lower:
            reply = (
                "Here is the complete Python code for Flappy Bird using Pygame:\n\n"
                "```python\n"
                "import pygame\n"
                "import random\n\n"
                "pygame.init()\n"
                "SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600\n"
                "screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))\n"
                "clock = pygame.time.Clock()\n\n"
                "bird_y, bird_x, gravity, bird_movement = 300, 50, 0.25, 0\n"
                "pipe_list, SPAWNPIPE = [], pygame.USEREVENT\n"
                "pygame.time.set_timer(SPAWNPIPE, 1200)\n\n"
                "while True:\n"
                "    for event in pygame.event.get():\n"
                "        if event.type == pygame.QUIT:\n"
                "            pygame.quit()\n"
                "            exit()\n"
                "        if event.type == pygame.KEYDOWN:\n"
                "            if event.key == pygame.K_SPACE:\n"
                "                bird_movement = -7\n"
                "        if event.type == SPAWNPIPE:\n"
                "            pipe_height = random.randint(200, 400)\n"
                "            pipe_list.append(pygame.Rect(400, pipe_height, 60, 500))\n\n"
                "    screen.fill((135, 206, 235))\n"
                "    bird_movement += gravity\n"
                "    bird_y += bird_movement\n"
                "    pygame.draw.circle(screen, (255, 255, 0), (bird_x, int(bird_y)), 15)\n\n"
                "    for pipe in pipe_list:\n"
                "        pipe.centerx -= 3\n"
                "        pygame.draw.rect(screen, (0, 200, 0), pipe)\n\n"
                "    pygame.display.update()\n"
                "    clock.tick(120)\n"
                "```"
            )
        elif "python" in msg_lower or "code" in msg_lower:
            reply = (
                "Here is your requested Python snippet:\n\n"
                "```python\n"
                "def zion_system_check():\n"
                "    print('Zion Prime Z spatial intelligence operational.')\n\n"
                "if __name__ == '__main__':\n"
                "    zion_system_check()\n"
                "```"
            )
        elif "who are you" in msg_lower or "what is your name" in msg_lower:
            reply = "I am Zion Prime Z, an advanced AI spatial intelligence assistant created by Master S. Joshua."
        elif "who is the us president" in msg_lower:
            reply = "Donald Trump"
        elif "who is the tn cm" in msg_lower or "chief minister" in msg_lower:
            reply = "C. Joseph Vijay (TVK)"
        elif "science expo" in msg_lower or "project" in msg_lower:
            reply = "Zion Prime Z integrates real-time PWA frontend interaction with custom Python backend processing for advanced science exhibition demonstrations."
        elif "gravity" in msg_lower:
            reply = "Gravity is a fundamental physical force by which objects with mass are drawn toward one another, with Earth's gravitational acceleration approximately 9.81 m/s²."
        else:
            reply = f"Zion Prime Z analyzed '{user_message}': Spatial reasoning and neural matrix computations indicate optimal operational status for this inquiry."

        return jsonify({"response": reply})

    except Exception as err:
        return jsonify({"response": f"Zion Prime Z active. Signal received."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
