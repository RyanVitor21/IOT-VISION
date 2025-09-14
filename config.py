# Fonte da câmera: 0 = webcam principal | 1 = outra câmera | ou URL de RTSP
CAMERA_SOURCE = 0

# Modelo YOLOv8 (detecção de objetos - mais leve que pose)
MODEL_NAME = "yolov8s.pt"  # pode trocar por 'yolov8n.pt' se quiser mais leve ainda

# Limiar de confiança
CONFIDENCE_THRESHOLD = 0.5

# Mostrar janela de vídeo
SHOW_VIDEO = True

# Porta da API (se usar no futuro)
API_PORT = 8000

# Nome do projeto
APP_NAME = "Vision IoT - Contagem de Pessoas"

# Intervalo de envio de dados para o Ubidots (segundos)
SEND_INTERVAL = 5
