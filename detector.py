# detector.py
import cv2
import time
import requests
from ultralytics import YOLO
from config import MODEL_NAME, CONFIDENCE_THRESHOLD, CAMERA_SOURCE, SHOW_VIDEO

# Variáveis globais para contagem
total_count = 0
inside_count = 0   # dentro da zona proibida
outside_count = 0  # fora da zona proibida

# Configurações do Ubidots
UBIDOTS_TOKEN = "BBUS-LYbWdeRmn4ZvHbILBPbWB5REjmcDid"  # 🔐 Substitua pelo seu token
DEVICE_LABEL = "vision-iot-sala"

# Variáveis no Ubidots
VARIABLE_TOTAL = "people_total"
VARIABLE_INSIDE = "people_inside"
VARIABLE_OUTSIDE = "people_outside"

# URLs de envio
URL_TOTAL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{VARIABLE_TOTAL}/values"
URL_INSIDE = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{VARIABLE_INSIDE}/values"
URL_OUTSIDE = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{VARIABLE_OUTSIDE}/values"

SEND_INTERVAL = 30  # segundos entre envios

# 🔴 Defina a zona proibida: (x1, y1, x2, y2)
FORBIDDEN_ZONE = (0, 0, 300, 500)  # Ajuste conforme sua cena

def send_to_ubidots():
    """
    Envia todos os contadores em uma ÚNICA requisição para o Ubidots
    """
    global total_count, inside_count, outside_count

    # Prepara payload com múltiplos campos
    payload = {
        "people_total": total_count,
        "people_inside": inside_count,
        "people_outside": outside_count
    }

    # Usa o endpoint de múltiplos valores (para o dispositivo inteiro)
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200 or response.status_code == 201:
            print(f"✅ Enviado ao Ubidots: Total={total_count}, Dentro={inside_count}, Fora={outside_count}")
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Falha ao enviar: {e}")

def is_in_forbidden_zone(x, y):
    """
    Verifica se o ponto (x, y) está dentro da zona proibida
    """
    x1, y1, x2, y2 = FORBIDDEN_ZONE
    return x1 <= x <= x2 and y1 <= y <= y2

def run_detection():
    global total_count, inside_count, outside_count

    # Carrega o modelo YOLOv8
    print("🔄 Carregando modelo YOLOv8...")
    model = YOLO(MODEL_NAME)  # 'yolov8s.pt'
    print("✅ Modelo carregado!")

    # Abre a câmera
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    if not cap.isOpened():
        print("❌ Erro ao abrir a câmera.")
        return

    # ✅ Define resolução (opcional, se sua câmera suportar)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("🎥 Iniciando detecção... Pressione 'q' para sair.")

    last_sent = 0  # último envio

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Falha ao ler frame.")
            break


        # Reinicia contadores
        total_count = 0
        inside_count = 0
        outside_count = 0

        # Roda a detecção
        results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)

        # Processa os resultados
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if cls == 0:  # 0 = 'person'
                    total_count += 1

                    # Coordenadas da caixa
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x = (x1 + x2) // 2
                    center_y = y2  # base do pé (mais estável)

                    # Verifica se está dentro da zona
                    if is_in_forbidden_zone(center_x, center_y):
                        color = (0, 0, 255)  # vermelho
                        label = "ALERTA: ZONA PROIBIDA"
                        inside_count += 1
                    else:
                        color = (0, 255, 0)  # verde
                        label = "Pessoa"
                        outside_count += 1

                    # Desenha caixa e rótulo
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Desenha a zona proibida (translúcida)
        overlay = frame.copy()
        x1, y1, x2, y2 = FORBIDDEN_ZONE
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

        # Mostra contagens no vídeo (canto superior esquerdo)
        cv2.putText(frame, f'Total: {total_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f'Dentro: {inside_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f'Fora: {outside_count}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # ✉️ Envio periódico para o Ubidots
        current_time = time.time()
        if current_time - last_sent >= SEND_INTERVAL:
            send_to_ubidots()
            last_sent = current_time

        if SHOW_VIDEO:
            cv2.imshow("Vision IoT - Monitoramento com Zona Proibida", frame)

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_detection()