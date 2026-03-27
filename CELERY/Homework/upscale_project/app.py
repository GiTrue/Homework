import io
from flask import Flask, request, jsonify, send_file
from tasks import upscale_task, celery_app
from celery.result import AsyncResult

app = Flask(__name__)

@app.post('/upscale')
def post_upscale():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    image_bytes = file.read()
    
    # Запускаем фоновую задачу
    task = upscale_task.delay(image_bytes)
    return jsonify({"task_id": task.id}), 201

@app.get('/tasks/<task_id>')
def get_status(task_id):
    result = AsyncResult(task_id, app=celery_app)
    response = {"status": result.status}
    
    if result.ready():
        if result.successful():
            response["link"] = f"/processed/{task_id}"
        else:
            response["error"] = str(result.result)
            
    return jsonify(response)

@app.get('/processed/<task_id>')
def get_file(task_id):
    result = AsyncResult(task_id, app=celery_app)
    if not result.ready():
        return jsonify({"error": "Task not ready"}), 404
    
    # Достаем байты из результата Celery
    img_io = io.BytesIO(result.result)
    return send_file(img_io, mimetype='image/png', download_name='upscaled.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)