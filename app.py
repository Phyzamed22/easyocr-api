from flask import Flask, request, jsonify
import easyocr
import numpy as np
import cv2

app = Flask(__name__)
reader = easyocr.Reader(['en'])
@app.route('/')
def home():
    return "EasyOCR API is running!"

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    img = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    result = reader.readtext(img)
    extracted_text = " ".join([text[1] for text in result])

    return jsonify({'text': extracted_text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port or default to 10000
    app.run(host="0.0.0.0", port=port)
