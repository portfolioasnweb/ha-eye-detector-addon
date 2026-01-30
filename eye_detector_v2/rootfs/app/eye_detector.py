import cv2
import mediapipe as mp
import time
import requests
import os
import json
import numpy as np
from scipy.spatial import distance as dist

# Força o log a aparecer imediatamente
def log(msg):
    print(f"[Eye Detector V2] {msg}", flush=True)

log("Iniciando motor de detecção...")

# Configurações básicas
OPTIONS_PATH = "/data/options.json"
HASSIO_TOKEN = os.getenv('SUPERVISOR_TOKEN')
API_URL = "http://supervisor/core/api/states/binary_sensor.eye_detector_status"

# Carrega URL
try:
    with open(OPTIONS_PATH) as f:
        RTSP_URL = json.load(f).get("rtsp_url")
except:
    RTSP_URL = None

if not RTSP_URL:
    log("ERRO: URL RTSP não configurada!")
    time.sleep(60)
    exit(1)

# Inicializa MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

cap = cv2.VideoCapture(RTSP_URL)

while True:
    success, frame = cap.read()
    if not success:
        log("Falha no sinal RTSP. Reconectando...")
        time.sleep(5)
        cap = cv2.VideoCapture(RTSP_URL)
        continue

    # Processamento EAR (mesma lógica anterior)
    # ... (seu código de detecção aqui)
    
    time.sleep(0.05)
