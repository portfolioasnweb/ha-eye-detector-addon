#!/usr/bin/with-contenv sh
set -e

echo "[Eye Detector V2] Iniciando o ambiente..."

# O arquivo eye_detector.py foi copiado para a raiz (/) pelo Dockerfile
python3 /eye_detector.py
