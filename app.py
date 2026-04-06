import os
import torch
import scipy.io.wavfile
from flask import Flask, request, render_template, jsonify
from audiocraft.models import MusicGen

app = Flask(__name__)

# Креирање папка за аудио
audio_dir = os.path.join('static', 'audio')
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)

print("--- Вчитувам MusicGen модел (Small)... ---")
model = MusicGen.get_pretrained('facebook/musicgen-small')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'LATIVM beat')

        # 8 секунди за подобар квалитет
        model.set_generation_params(duration=8)
        wav = model.generate([prompt], progress=True)

        audio_data = wav[0].cpu().numpy()
        sampling_rate = 32000

        file_name = "generated_output.wav"
        full_path = os.path.join(audio_dir, file_name)

        # Scipy е најсигурен за CPU средини
        scipy.io.wavfile.write(full_path, sampling_rate, audio_data.T)

        return jsonify({
            "status": "success",
            "audio_url": f"/static/audio/{file_name}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # ОБАВЕЗНО порта 7860 за Hugging Face
    app.run(host='0.0.0.0', port=7860)