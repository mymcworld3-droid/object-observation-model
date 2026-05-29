import os
import base64
from flask import Flask, request, send_file, jsonify
import json

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/train', mode=['POST'])
def train_model():
    data = request.get_json()
    if not data:
        return jsonify({"error": "無有效數據"}), 400

    image_data = data['image']
    annotations = data['annotations']

    # 1. 解碼前端傳來的 Base64 圖片並儲存
    header, encoded = image_data.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    
    os.makedirs('dataset', exist_ok=True)
    with open("dataset/current_frame.jpg", "wb") as f:
        f.write(img_bytes)

    # 2. 將前端畫好的方框座標寫入標註檔案 (JSON/YOLO)
    with open("dataset/annotations.json", "w") as f:
        json.dump(annotations, f)

    #🔥 3. 在此處觸穿 TensorFlow / MediaPipe Model Maker 進行增量訓練
    # (註：由於 Render 免費版沒有 GPU，此處通常會執行輕量化的 1~2 輪 Epochs 快照)
    # 這裡我們模擬訓練完成，生成一個虛擬的模型檔案回傳
    model_path = "dataset/surviv_model.tflite"
    with open(model_path, "w") as f:
        f.write("TF-Lite-Dummy-Model-Data")

    # 4. 將訓練完的模型檔案直接回傳給平板下載
    return send_file(model_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
