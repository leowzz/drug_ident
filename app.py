from flask import Flask, request
from utils.tts import speech
from utils.orc import recognition

app = Flask(__name__, static_folder='static', static_url_path='/')


@app.route('/ocr', methods=['POST'])
def ocr_():
    img = request.files.get('image')
    print(img)
    # 识别文本
    res = recognition(img)

    return res


@app.route('/ocr_speech', methods=['POST'])
def ocr_tts():
    img = request.files.get('image')
    print(img)
    # 识别文本
    res = recognition(img)
    # 使用文本生成语音 url
    res['url'] = speech(res.get("text"))

    return res


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run()
