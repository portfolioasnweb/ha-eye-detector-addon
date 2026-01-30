ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala as bibliotecas Python necessárias
RUN pip3 install --no-cache-dir --break-system-packages \
    numpy \
    opencv-python-headless \
    mediapipe \
    requests \
    scipy

# Copia o conteúdo de rootfs para a raiz [/] do container
COPY rootfs/ /

# Garante permissão de execução no script
RUN chmod a+x /run.sh
