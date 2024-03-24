from flask import Flask, render_template, request,jsonify
import cv2
import base64
import numpy as np
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit', methods=['POST'])
def edit():
    image_data = request.form['image_data']
    image_bytes = base64.b64decode(image_data.split(',')[1])
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    operation = request.form['operation']
    if operation == 'crop':
        x1 = int(request.form['x1'])
        y1 = int(request.form['y1'])
        x2 = int(request.form['x2'])
        y2 = int(request.form['y2'])
        image = image[y1:y2, x1:x2]
    elif operation == 'rotate':
        angle = int(request.form['rotate_angle'])
        rows, cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        image = cv2.warpAffine(image, M, (cols, rows))
    elif operation == 'blur':
        image = cv2.GaussianBlur(image, (5, 5), 0)
    elif operation == 'text':
        text = request.form['text_data']
        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (10, 30)
        font_scale = 1
        color = (0, 0, 0)
        thickness = 2
        image = cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
    elif operation == 'contrast':
        alpha = float(request.form['contrast_value'])
        image = cv2.convertScaleAbs(image, alpha=alpha)

    _, image_data = cv2.imencode('.jpg', image)
    image_data = base64.b64encode(image_data).decode('utf-8')
    return jsonify({'image_data': image_data})


if __name__ == '__main__':
    app.run(debug=True)