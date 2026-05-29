import os
from flask import Flask

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    # 讀取同目錄下的 index.html 前端面板
    return app.send_static_file('index.html')

if __name__ == '__main__':
    # 綁定連接埠，完美適配 Render 部署環境
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
