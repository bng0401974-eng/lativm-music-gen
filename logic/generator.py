import torch
from audiocraft.models import MusicGen
import io
import scipy.io.wavfile
import base64


class LativmGenerator:
    def __init__(self):
        self.model = None

    def load_model(self):
        if self.model is None:
            print(">>> Вчитувам MusicGen модел во меморија...")
            self.model = MusicGen.get_pretrained('facebook/musicgen-small')
        return self.model

    def generate_audio(self, prompt, duration, temperature):
        m = self.load_model()
        m.set_generation_params(duration=duration, temperature=temperature)

        # Генерирање на сигналот
        wav = m.generate([prompt])

        # Конверзија во Base64 за пренос до фронтенд
        byte_io = io.BytesIO()
        scipy.io.wavfile.write(byte_io, 32000, wav[0, 0].cpu().numpy())
        return base64.b64encode(byte_io.getvalue()).decode('utf-8')


# Инстанца што ќе ја користиме во app.py
lativm_ai = LativmGenerator()