ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY rootfs /

RUN pip install --no-cache-dir \
    numpy \
    opencv-python-headless \
    mediapipe

RUN chmod +x /run.sh

CMD ["/run.sh"]
