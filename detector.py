import cv2
import time
from ultralytics import YOLO
from camera import get_video_capture
from config import MODEL_NAME, CONFIDENCE_THRESHOLD, SHOW_VIDEO, APP_NAME, SEND_INTERVAL
from supabase_client import send_to_supabase

# Inicializa contadores
total_count = 0
inside_count = 0
outside_count = 0
last_sent = time.time()

# Carregar modelo YOLO
print("📦 Carregando modelo YOLO...")
model = YOLO(MODEL_NAME)

cap = get_video_capture()

if cap:
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Não conseguiu capturar frame.")
                break

            # Detecta pessoas (classe 0 do COCO)
            results = model(frame, verbose=False, conf=CONFIDENCE_THRESHOLD)
            people_detected = [r for r in results[0].boxes if int(r.cls[0]) == 0]

            # Atualiza contadores
            total_count = len(people_detected)
            inside_count = total_count // 2
            outside_count = total_count - inside_count

            # Mostra na tela
            if SHOW_VIDEO:
                cv2.putText(frame, f"Total: {total_count}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Inside: {inside_count}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                cv2.putText(frame, f"Outside: {outside_count}", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow(APP_NAME, frame)

            # Enviar dados periodicamente
            current_time = time.time()
            if current_time - last_sent >= SEND_INTERVAL:
                try:
                    send_to_supabase(total_count, inside_count, outside_count)
                    last_sent = current_time
                except Exception as e:
                    print("⚠️ Erro ao enviar para Supabase:", e)

            # Sair com 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("⏹️ Interrompido pelo usuário.")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Recursos liberados. Programa finalizado.")
