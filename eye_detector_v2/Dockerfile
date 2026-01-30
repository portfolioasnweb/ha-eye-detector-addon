ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:latest
FROM ${BUILD_FROM}

# Instala dependências
RUN apt-get update && apt-get install -y \
    python3 python3-pip libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala bibliotecas
RUN pip3 install --no-cache-dir --break-system-packages \
    numpy opencv-python-headless mediapipe requests scipy

# Copia os arquivos
COPY rootfs/ /
RUN chmod a+x /etc/services.d/eye_detector/run
