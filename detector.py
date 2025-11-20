import cv2
import time
import requests
from ultralytics import YOLO
from config import MODEL_NAME, CONFIDENCE_THRESHOLD, CAMERA_SOURCE, SHOW_VIDEO

total_count = 0
inside_count = 0 
outside_count = 0 

UBIDOTS_TOKEN = "BBUS-LYbWdeRmn4ZvHbILBPbWB5REjmcDid"
DEVICE_LABEL = "vision-iot-sala"

VARIABLE_TOTAL = "people_total"
VARIABLE_INSIDE = "people_inside"
VARIABLE_OUTSIDE = "people_outside"

URL_TOTAL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{VARIABLE_TOTAL}/values"
URL_INSIDE = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{VARIABLE_INSIDE}/values"
URL_OUTSIDE = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{VARIABLE_OUTSIDE}/values"

SEND_INTERVAL = 10

# Zona proibida: centralizada horizontalmente (~500px de largura), altura 100% (toda a frame).
# Valores baseados na resolução definida no código (1280x720). Ajuste se alterar CAPTURE size.
ZONE_WIDTH = 500
FRAME_WIDTH_DEFAULT = 1280
FRAME_HEIGHT_DEFAULT = 720
_center_x = FRAME_WIDTH_DEFAULT // 2
_x1 = max(0, _center_x - ZONE_WIDTH // 2)
_x2 = min(FRAME_WIDTH_DEFAULT, _x1 + ZONE_WIDTH)
FORBIDDEN_ZONE = (_x1, 0, _x2, FRAME_HEIGHT_DEFAULT)

def send_to_ubidots():
    """
    Envia todos os contadores em uma ÚNICA requisição para o Ubidots
    """
    global total_count, inside_count, outside_count

    payload = {
        "people_total": total_count,
        "people_inside": inside_count,
        "people_outside": outside_count
    }

    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200 or response.status_code == 201:
            print(f"Enviado ao Ubidots: Total={total_count}, Dentro={inside_count}, Fora={outside_count}")
        else:
            print(f"Erro {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Falha ao enviar: {e}")

def is_in_forbidden_zone(x, y):
    """
    Verifica se o ponto (x, y) está dentro da zona proibida
    """
    x1, y1, x2, y2 = FORBIDDEN_ZONE
    return x1 <= x <= x2 and y1 <= y <= y2

def run_detection():
    global total_count, inside_count, outside_count

    print("Carregando modelo YOLOv8...")
    model = YOLO(MODEL_NAME)
    print("Modelo carregado!")

    cap = cv2.VideoCapture(CAMERA_SOURCE)
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("Iniciando detecção... Pressione 'q' para sair.")

    last_sent = 0 

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao ler frame.")
            break


        total_count = 0
        inside_count = 0
        outside_count = 0

        results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if cls == 0:  
                    total_count += 1

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x = (x1 + x2) // 2
                    center_y = y2

                    if is_in_forbidden_zone(center_x, center_y):
                        color = (0, 0, 255)
                        label = "ALERTA: ZONA PROIBIDA"
                        inside_count += 1
                    else:
                        color = (0, 255, 0)
                        label = "Pessoa"
                        outside_count += 1

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        overlay = frame.copy()
        x1, y1, x2, y2 = FORBIDDEN_ZONE
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

        cv2.putText(frame, f'Total: {total_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f'Dentro: {inside_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f'Fora: {outside_count}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        current_time = time.time()
        if current_time - last_sent >= SEND_INTERVAL:
            send_to_ubidots()
            last_sent = current_time

        if SHOW_VIDEO:
            cv2.imshow("Vision IoT - Monitoramento com Zona Proibida", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_detection()