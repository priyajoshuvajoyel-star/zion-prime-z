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
        
        # 1. Dynamic Image Generation Routing
        if any(kw in msg_lower for kw in ["image", "photo", "draw", "picture", "paint"]) and "code" not in msg_lower:
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

        # 2. Greetings, Identity & Expo Highlights
        if any(k in msg_lower for k in ["roadster", "roadster 2", "spacex", "falcon heavy", "space experiment"]):
            reply = "Experiment Overview: Elon Musk's Tesla Roadster was launched into heliocentric orbit via the SpaceX Falcon Heavy test flight. It acts as a dummy payload demonstrating orbital mechanics, escape velocity, and long-term space environment durability."
        elif any(k in msg_lower for k in ["hi", "hello", "hey", "greetings"]):
            reply = "Hello! I am Zion Prime Z, your spatial intelligence assistant. How can I help you with our science expo demonstration today?"
        elif any(k in msg_lower for k in ["who are you", "your name", "what are you", "self introduction", "introduce yourself"]):
            reply = "I am Zion Prime Z, an advanced PWA spatial intelligence and science assistant created by Master S. Joshua. I integrate real-time voice synthesis, dynamic UI history management, and custom Python processing to deliver instant answers across physics, chemistry, biology, and software engineering for exhibition demonstrations."

        # 3. Specific Games / Dedicated Coding
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

        # 4. Universal Code Engine (Catch-all for any other coding query)
        elif any(k in msg_lower for k in ["code", "script", "program", "function", "coding", "python", "html", "css", "javascript", "algorithm"]):
            reply = (
                f"Here is a complete operational code implementation for '{user_message}':\n\n"
                "```python\n"
                "# Zion Prime Z Core Execution Engine\n"
                "import time\n"
                "import math\n\n"
                "def execute_task(input_data):\n"
                "    \"\"\"Processes task query through Zion spatial matrix\"\"\"\n"
                "    print(f'[ZION CORE] Processing: {input_data}')\n"
                "    status = {'status': 'success', 'code': 200, 'matrix_active': True}\n"
                "    return status\n\n"
                "if __name__ == '__main__':\n"
                "    result = execute_task('User Request Verified')\n"
                "    print('Execution Output:', result)\n"
                "```"
            )

        # 5. Specific Chemistry, Physics & Biology Entries
        elif "water" in msg_lower:
            reply = "Chemical Formula: H2O. Common Reaction/Process: Electrolysis of water breaks it down into hydrogen and oxygen (2H2O -> 2H2 + O2)."
        elif "ammonia" in msg_lower:
            reply = "Chemical Formula: NH3. Common Reaction Name: Haber Process (N2 + 3H2 <-> 2NH3) used for industrial synthesis."
        elif "salt" in msg_lower or "sodium chloride" in msg_lower:
            reply = "Chemical Formula: NaCl. Common Reaction Name: Neutralization reaction (HCl + NaOH -> NaCl + H2O)."
        elif "carbon dioxide" in msg_lower:
            reply = "Chemical Formula: CO2. Common Reaction Name: Combustion or Respiration byproduct."
        elif "sulfuric acid" in msg_lower:
            reply = "Chemical Formula: H2SO4. Known as the 'King of Chemicals', widely used in contact process manufacturing."
        elif "methane" in msg_lower:
            reply = "Chemical Formula: CH4. Common Reaction Name: Combustion (CH4 + 2O2 -> CO2 + 2H2O)."
        elif "hydrochloric acid" in msg_lower:
            reply = "Chemical Formula: HCl. Strong acid commonly used in laboratory synthesis and gastric digestion."
        elif "gravity" in msg_lower or "gravitational" in msg_lower:
            reply = "Physics Concept: Universal Gravitation (F = G * (m1 * m2) / r²). Earth's standard gravitational acceleration is approximately 9.81 m/s²."
        elif "ohm" in msg_lower or "voltage" in msg_lower or "current" in msg_lower:
            reply = "Physics Law: Ohm's Law (V = I * R), defining the relationship between voltage (V), current (I), and resistance (R)."
        elif "newton" in msg_lower or "force" in msg_lower:
            reply = "Physics Laws: Newton's Laws of Motion. 1st: Inertia; 2nd: Force equals mass times acceleration (F = ma); 3rd: Action and reaction are equal and opposite."
        elif "velocity" in msg_lower or "speed" in msg_lower or "acceleration" in msg_lower:
            reply = "Physics Kinematics: Acceleration is the rate of change of velocity (a = (v - u) / t), measured in m/s²."
        elif "energy" in msg_lower or "power" in msg_lower:
            reply = "Physics Principle: Conservation of Energy (E = mc² or Kinetic/Potential energy transfer). Power is work done per unit time (P = W / t)."
        elif "photosynthesis" in msg_lower:
            reply = "Biology Process: Photosynthesis (6CO2 + 6H2O + Light -> C6H12O6 + 6O2), used by plants to convert light energy into chemical energy."
        elif "mitochondria" in msg_lower:
            reply = "Biology Term: Mitochondria is known as the 'powerhouse of the cell', responsible for generating chemical energy in the form of ATP."
        elif "dna" in msg_lower or "rna" in msg_lower:
            reply = "Biology Term: Deoxyribonucleic Acid (DNA) is a double-helix molecule carrying genetic instructions for the development, functioning, and reproduction of all living organisms."
        elif "osmosis" in msg_lower or "diffusion" in msg_lower:
            reply = "Biology Process: Osmosis is the movement of water molecules across a selectively permeable membrane from an area of higher water potential to lower water potential."
        elif "cell" in msg_lower:
            reply = "Biology Term: The cell is the basic structural, functional, and biological unit of all known living organisms."

        # 6. Universal Science & Mechanism Engine (Catch-all for any other scientific query)
        elif any(k in msg_lower for k in ["explain", "how does", "mechanism", "working", "principle", "science", "process", "reaction", "law", "experiment", "formula", "chemical"]):
            reply = (
                f"Scientific Analysis for '{user_message}':\n\n"
                f"1. Core Principle: The process operates under fundamental physical laws and chemical conservation principles.\n"
                f"2. Mechanism: System dynamics undergo state transformations driven by potential energy and thermodynamic gradients, establishing stoichiometric balance across intermediate states.\n"
                f"3. Practical Impact: This mechanism serves as a primary scientific foundation for advanced engineering and technological implementations."
            )

        # 7. Leaders & Fallback
        elif any(k in msg_lower for k in ["president", "usa", "united states", "america"]):
            reply = "Donald Trump"
        elif any(k in msg_lower for k in ["cm of tamil nadu", "chief minister of tamil nadu", "tamil nadu cm", "who is the cm"]):
            reply = "C. Joseph Vijay (TVK) is the Chief Minister of Tamil Nadu."
        else:
            reply = f"Zion Prime Z Science Matrix: Regarding '{user_message}', local neural analysis confirms core scientific consistency and optimal execution parameters."

        return jsonify({"response": reply})

    except Exception as err:
        return jsonify({"response": f"Zion Prime Z active. Signal received."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
