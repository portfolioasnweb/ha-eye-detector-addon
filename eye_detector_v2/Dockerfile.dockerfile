FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    mediapipe \
    opencv-python-headless \
    paho-mqtt \
    numpy \
    requests

COPY rootfs/ /
RUN chmod +x /run.sh

CMD ["/run.sh"]