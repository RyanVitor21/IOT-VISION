import cv2
from config import CAMERA_SOURCE, SHOW_VIDEO, APP_NAME

def get_video_capture():
    """
    Inicializa a captura de vídeo.
    """
    cap = cv2.VideoCapture(CAMERA_SOURCE)

    if not cap.isOpened():
        print("❌ Erro: Não foi possível acessar a câmera.")
        return None

    print("✅ Câmera conectada com sucesso.")
    return cap

if __name__ == "__main__":
    cap = get_video_capture()

    if cap:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Não conseguiu capturar frame.")
                break

            if SHOW_VIDEO:
                cv2.imshow(APP_NAME, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
