from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
from flask_cors import CORS
import cv2

app = Flask(__name__)
CORS(app)

# Set up Tesseract OCR
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Modify this path to your Tesseract installation

# Initialize the camera

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        if 'image' not in request.files:
            cv2.VideoCapture(0)  # Use 0 for the default camera, you can change this value
            return jsonify({'error': 'No image uploaded'}), 400

        image = request.files['image']

        if image.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        if not allowed_file(image.filename):
            return jsonify({'error': 'Invalid file format'}), 400

        # Perform text extraction from the uploaded image
        extracted_text = ocr_text(image)

        return jsonify({'extracted_text': extracted_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

def ocr_text(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text

if __name__ == '__main__':
    app.run(debug=True)
