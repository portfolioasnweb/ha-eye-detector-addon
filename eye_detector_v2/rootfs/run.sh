#!/usr/bin/with-contenv sh
set -e

echo "[Eye Detector V2] Iniciando..."

# O arquivo eye_detector.py deve estar na raiz / devido ao COPY do Dockerfile
exec python3 /eye_detector.py
