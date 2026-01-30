ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala as bibliotecas Python
# Adicionado --break-system-packages para permitir instalação global em containers modernos
RUN pip3 install --no-cache-dir --break-system-packages \
    numpy \
    opencv-python-headless \
    mediapipe

WORKDIR /app
COPY rootfs/ /

# Garante que o script de inicialização tenha permissão de execução
RUN chmod a+x /run.sh

CMD ["/run.sh"]
