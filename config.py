# config.py

# Fonte da câmera: 0 1 url
CAMERA_SOURCE = 0

# Modelo YOLOv8 (detecção de objetos - mais leve que pose)
MODEL_NAME = "yolov8s.pt"  # ou 'yolov8s.pt' se quiser mais precisão

# Limiar de confiança
CONFIDENCE_THRESHOLD = 0.5

# Mostrar janela de vídeo
SHOW_VIDEO = True

# Porta da API (se usar no futuro)
API_PORT = 8000

# Nome do projeto
APP_NAME = "Vision IoT - Contagem de Pessoas"