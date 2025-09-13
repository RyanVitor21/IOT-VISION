# Vision IoT - Contagem de Pessoas 👁️🤖

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-vision-green)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Detection-red)
![IoT](https://img.shields.io/badge/IoT-Ubidots-orange)

## 📌 Descrição
**Vision IoT** é um sistema em **Python** que utiliza **YOLOv8** para detectar e contar pessoas em tempo real via câmera (notebook, PC ou externa).  
Além da contagem, o sistema identifica indivíduos dentro de uma **zona proibida** e envia métricas (total, dentro, fora) automaticamente para o **Ubidots**, possibilitando integração com soluções IoT e automação.

---

## 🎥 Demonstração


---

## ✨ Funcionalidades
- 📷 Captura de vídeo em tempo real via câmera local ou externa  
- 👥 Detecção e contagem automática de pessoas com YOLOv8  
- 🚫 Monitoramento de **zona proibida** (alerta visual no frame)  
- ☁️ Envio de métricas para **Ubidots** em intervalos configuráveis  
- 🖥️ Exibição em janela com overlays de contagem e zona destacada  
- 🌐 Estrutura pronta para API com **FastAPI** e painel via **Streamlit**  

---

## 🛠️ Tecnologias Utilizadas
- [Python 3.10+](https://www.python.org/)  
- [OpenCV](https://opencv.org/)  
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)  
- [MediaPipe](https://developers.google.com/mediapipe)  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [Uvicorn](https://www.uvicorn.org/)  
- [Streamlit](https://streamlit.io/)  
- [NumPy](https://numpy.org/)  
- [Requests](https://docs.python-requests.org/en/latest/)  
- [Ubidots](https://ubidots.com/)  

---

