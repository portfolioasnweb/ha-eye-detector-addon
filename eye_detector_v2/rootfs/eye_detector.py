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

# Marcos dos olhos (MediaPipe Mesh)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
EAR_THRESHOLD = 0.21 

def get_ear(eye_points):
    v1 = dist.euclidean(eye_points[1], eye_points[5])
    v2 = dist.euclidean(eye_points[2], eye_points[4])
    h = dist.euclidean(eye_points[0], eye_points[3])
    return (v1 + v2) / (2.0 * h)

def update_ha(is_closed):
    headers = {"Authorization": f"Bearer {HASSIO_TOKEN}", "Content-Type": "application/json"}
    data = {"state": "on" if is_closed else "off", "attributes": {"device_class": "problem", "friendly_name": "Olhos Fechados"}}
    try:
        requests.post(API_URL, headers=headers, json=data, timeout=5)
    except:
        pass

# Carregar URL configurada na interface do HA
try:
    with open(OPTIONS_PATH) as f:
        config = json.load(f)
        RTSP_URL = config.get("rtsp_url")
except:
    RTSP_URL = None

if not RTSP_URL:
    print("[Erro] URL RTSP não configurada nos Ajustes!", flush=True)
    while True: time.sleep(60)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

cap = cv2.VideoCapture(RTSP_URL)
last_state = None

while True:
    success, frame = cap.read()
    if not success:
        time.sleep(5)
        cap = cv2.VideoCapture(RTSP_URL)
        continue

    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    eyes_closed = False
    if results.multi_face_landmarks:
        mesh_coords = np.array([[p.x, p.y] for p in results.multi_face_landmarks[0].landmark])
        left_ear = get_ear(mesh_coords[LEFT_EYE])
        right_ear = get_ear(mesh_coords[RIGHT_EYE])
        if (left_ear + right_ear) / 2.0 < EAR_THRESHOLD:
            eyes_closed = True

    if eyes_closed != last_state:
        update_ha(eyes_closed)
        last_state = eyes_closed
        print(f"Estado: {'Fechado' if eyes_closed else 'Aberto'}", flush=True)
    
    time.sleep(0.05)
