import cv2
from config import CAMERA_SOURCE

def get_video_capture():
    """
    Inicializa a captura de vídeo.
    """
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    
    if not cap.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return None
        
    print("Câmera conectada com sucesso.")
    return cap