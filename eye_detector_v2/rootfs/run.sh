#!/usr/bin/with-contenv sh
set -e

echo "[Eye Detector V2] Iniciando serviço de detecção..."

# Executa o script python que está na raiz
python3 /eye_detector.py
