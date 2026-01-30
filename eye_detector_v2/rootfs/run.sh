#!/usr/bin/with-contenv sh
set -e

echo "[Eye Detector V2] Iniciando serviço..."

# Executa o python que foi copiado para a raiz 
python3 /eye_detector.py
