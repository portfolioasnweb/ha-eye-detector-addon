ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# 1. Instala dependências do sistema necessárias para o OpenCV e MediaPipe
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Instala as bibliotecas Python
# A flag --break-system-packages é essencial em versões recentes do Debian/Python
RUN pip3 install --no-cache-dir --break-system-packages \
    numpy \
    opencv-python-headless \
    mediapipe

WORKDIR /app

# 3. Copia o conteúdo de 'rootfs' para a raiz do container
# O arquivo 'rootfs/run.sh' vai parar em '/run.sh'
COPY rootfs/ /

# 4. Garante permissão de execução (CRUCIAL se você criou o arquivo no Windows)
RUN chmod a+x /run.sh

CMD ["/run.sh"]
