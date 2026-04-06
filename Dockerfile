
 # 1. ОСНОВА
FROM python:3.9-bullseye

# 2. РАБОТНА ПАПКА
WORKDIR /code

# 3. СИСТЕМСКИ ПАКЕТИ
RUN apt-get update && apt-get install -y \
    ffmpeg \
    pkg-config \
    build-essential \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# 4. ИНСТАЛАЦИЈА НА AV (Бинарна верзија)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir av==12.3.0 --only-binary=:all:

# 5. КОПИРАЊЕ НА ФАЈЛОВИТЕ
COPY . /code/

# 6. ГЛАВНИ БИБЛИОТЕКИ
RUN pip install --no-cache-dir flask torch torchaudio

# 7. AUDIOCRAFT + КОМПЛЕТНИ ЗАВИСНОСТИ (Сега и со TorchDiffEq)
RUN pip install --no-cache-dir git+https://github.com/facebookresearch/audiocraft.git --no-deps
RUN pip install --no-cache-dir \
    flashy \
    antlr4-python3-runtime \
    demucs \
    julius \
    dora-search \
    encodec \
    docopt \
    pesq \
    omegaconf \
    hydra-core \
    scipy \
    soundfile \
    huggingface_hub \
    sentencepiece \
    tqdm \
    requests \
    xformers \
    num2words \
    "spacy>=3.5.0,<3.8.0" \
    "pydantic<2.0" \
    einops \
    vector_quantize_pytorch \
    diffusers \
    transformers \
    accelerate \
    librosa \
    resampy \
    numba \
    torchdiffeq \
    torchmetrics \
    typing-extensions

    
# 8. СТАРТУВАЊЕ
CMD ["python", "/code/app.py"]