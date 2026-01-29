FROM ghcr.io/home-assistant/amd64-base:latest

ENV LANG C.UTF-8

RUN apk add --no-cache \
    python3 \
    py3-pip \
    libgl \
    libglib

WORKDIR /app

COPY rootfs /

RUN pip3 install --no-cache-dir \
    mediapipe \
    opencv-python \
    numpy

RUN chmod +x /run.sh

CMD ["/run.sh"]
