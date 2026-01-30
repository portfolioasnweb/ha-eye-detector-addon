import cv2
import mediapipe as mp
import time
import requests
import os
import json
import numpy as np
from scipy.spatial import distance as dist

# Função para print imediato no log do HA
def log(msg):
    print(f"[Eye Detector V2] {msg}", flush=True)

log("Carregando modelos e bibliotecas...")

# Configurações do Home Assistant
OPTIONS_PATH = "/data/options.json"
HASSIO_TOKEN = os.getenv('SUPERVISOR_TOKEN')
API_URL = "http://supervisor/core/api/states/binary_sensor.eye_detector_status"

# Marcos dos olhos no MediaPipe Face Mesh
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
EAR_THRESHOLD = 0.21  # Ajuste a sensibilidade aqui

def get_ear(eye_points):
    """Calcula a proporção de abertura do olho (Eye Aspect Ratio)"""
    v1 = dist.euclidean(eye_points[1], eye_points[5])
    v2 = dist.euclidean(eye_points[2], eye_points[4])
    h = dist.euclidean(eye_points[0], eye_points[3])
    return (v1 + v2) / (2.0 * h)

def update_ha(is_closed):
    """Envia o estado para o Home Assistant via API interna"""
    headers = {
        "Authorization": f"Bearer {HASSIO_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "state": "on" if is_closed else "off",
        "attributes": {
            "device_class": "problem",
            "friendly_name": "Fadiga: Olhos Fechados",
            "icon": "mdi:eye-off" if is_closed else "mdi:eye"
        }
    }
    try:
        requests.post(API_URL, headers=headers, json=data, timeout=5)
    except Exception as e:
        log(f"Erro ao comunicar com HA: {e}")

# Tenta carregar a URL RTSP configurada pelo usuário
try:
    with open(OPTIONS_PATH) as f:
        config = json.load(f)
        RTSP_URL = config.get("rtsp_url")
except Exception as e:
    log(f"Erro ao ler configurações: {e}")
    RTSP_URL = None

if not RTSP_URL:
    log("ERRO: URL RTSP não encontrada nos Ajustes do Add-on!")
    time.sleep(60)
    exit(1)

# Inicializa o MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True, 
    max_num_faces=1, 
    min_detection_confidence=0.5
)

log(f"Conectando ao stream: {RTSP_URL}")
cap = cv2.VideoCapture(RTSP_URL)
last_state = None

while True:
    success, frame = cap.read()
    
    if not success:
        log("Sinal da câmera perdido. Tentando reconectar em 5s...")
        time.sleep(5)
        cap = cv2.VideoCapture(RTSP_URL)
        continue

    # Redimensiona para melhorar a performance
    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    eyes_closed = False
    
    if results.multi_face_landmarks:
        # Pega as coordenadas dos marcos faciais
        mesh_coords = np.array([[p.x, p.y] for p in results.multi_face_landmarks[0].landmark])
        
        # Calcula EAR para ambos os olhos
        left_ear = get_ear(mesh_coords[LEFT_EYE])
        right_ear = get_ear(mesh_coords[RIGHT_EYE])
        avg_ear = (left_ear + right_ear) / 2.0

        if avg_ear < EAR_THRESHOLD:
            eyes_closed = True

    # Atualiza o HA apenas quando o estado muda
    if eyes_closed != last_state:
        update_ha(eyes_closed)
        last_state = eyes_closed
        log(f"Estado alterado: {'FECHADO' if eyes_closed else 'ABERTO'}")

    # Pequena pausa para aliviar a CPU
    time.sleep(0.05)
