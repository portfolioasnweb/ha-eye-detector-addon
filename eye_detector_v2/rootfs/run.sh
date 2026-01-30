#!/usr/bin/with-contenv sh
set -e

echo "[Eye Detector V2] Iniciando serviço..."

# Executa o python de forma que ele herde os sinais do sistema
exec python3 /eye_detector.py
