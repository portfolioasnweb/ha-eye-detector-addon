import cv2
import mediapipe as mp
import time
import requests
import os
import json
import numpy as np
from scipy.spatial import distance as dist

print("[Eye Detector V2] Script iniciado!", flush=True)

OPTIONS_PATH = "/data/options.json"
HASSIO_TOKEN = os.getenv('SUPERVISOR_TOKEN')
API_URL = "http://supervisor/core/api/states/binary_sensor.eye_detector_status"

# Função para calcular EAR
def get_ear(eye_points):
    v1 = dist.euclidean(eye_points[1], eye_points[5])
    v2 = dist.euclidean(eye_points[2], eye_points[4])
    h = dist.euclidean(eye_points[0], eye_points[3])
    return (v1 + v2) / (2.0 * h)

# Carregar URL das Opções
try:
    with open(OPTIONS_PATH) as f:
        config = json.load(f)
        RTSP_URL = config.get("rtsp_url")
except:
    RTSP_URL = None

if not RTSP_URL:
    print("[Erro] URL RTSP não configurada na aba Ajustes!", flush=True)
    while True: time.sleep(60)

# Setup MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

cap = cv2.VideoCapture(RTSP_URL)
last_state = None

while True:
    success, frame = cap.read()
    if not success:
        print("Reconectando ao RTSP...", flush=True)
        time.sleep(5)
        cap = cv2.VideoCapture(RTSP_URL)
        continue

    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    eyes_closed = False
    if results.multi_face_landmarks:
        # Lógica de detecção aqui...
        pass

    time.sleep(0.05)
