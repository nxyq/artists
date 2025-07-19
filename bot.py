from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/get')
def get_image():
    url = request.args.get('url')
    if not url:
        return "No URL provided", 400

    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = img.resize((32, 32))

        pixels = list(img.getdata())
        pixels.append([255, 255, 255])  # dummy pixel

        return jsonify(pixels)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 57554))
    app.run(host='0.0.0.0', port=port)
