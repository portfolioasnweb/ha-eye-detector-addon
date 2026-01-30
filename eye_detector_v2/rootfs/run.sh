#!/usr/bin/with-contenv sh
set -e

echo "[Eye Detector V2] Iniciando serviço..."

# Executa o python que está na raiz [/]
exec python3 /eye_detector.py
