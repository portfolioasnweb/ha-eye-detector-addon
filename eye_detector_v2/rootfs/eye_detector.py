import time
import sys

print("[Eye Detector V2] Script Python iniciado com sucesso!", flush=True)

try:
    while True:
        print("[Eye Detector V2] Monitoramento ativo...", flush=True)
        time.sleep(30)
except KeyboardInterrupt:
    print("[Eye Detector V2] Encerrando...")
    sys.exit(0)
