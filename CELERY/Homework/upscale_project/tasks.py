import cv2
import numpy as np
from celery import Celery
from cv2 import dnn_superres

# Настройка Celery
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

# Глобальная переменная для модели (синглтон внутри воркера)
scaler = None

def get_scaler():
    global scaler
    if scaler is None:
        scaler = dnn_superres.DnnSuperResImpl_create()
        scaler.readModel("models/EDSR_x2.pb")
        scaler.setModel("edsr", 2)
    return scaler

@celery_app.task(bind=True)
def upscale_task(self, image_bytes):
    # Декодируем байты в изображение OpenCV
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Апскейл
    result = get_scaler().upsample(img)
    
    # Кодируем обратно в байты (например, в формате PNG)
    _, buffer = cv2.imencode('.png', result)
    return buffer.tobytes()