from flask import Flask, render_template, request, jsonify
import torch
from audiocraft.models import MusicGen
import base64
import io
import scipy.io.wavfile

app = Flask(__name__)

# Инстанцирање на моделот
print("--- Вчитувам LATIVM MusicGen ---")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = MusicGen.get_pretrained('facebook/musicgen-small')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    duration = int(data.get('duration', 8))

    model.set_generation_params(duration=duration)
    wav = model.generate([prompt])

    byte_io = io.BytesIO()
    # MusicGen користи 32000Hz по стандард
    scipy.io.wavfile.write(byte_io, 32000, wav[0, 0].cpu().numpy())
    audio_b64 = base64.b64encode(byte_io.getvalue()).decode('utf-8')

    return jsonify({'audio': audio_b64})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)