import os
from flask import Flask, render_template, request, jsonify
from logic.generator import lativm_ai

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        duration = int(data.get('duration', 15))
        temp = float(data.get('temp', 1.0))

        audio_b64 = lativm_ai.generate_audio(prompt, duration, temp)
        return jsonify({'audio': audio_b64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Hugging Face и други сервери ја користат променливата PORT
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port)