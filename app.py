# app.py
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import base64
from io import BytesIO


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit', methods=['POST'])
def edit():
    img_data = request.files['image']
    img = Image.open(img_data)

    # Apply filters based on user inputs
    if 'rotate' in request.form:
        angle = int(request.form['rotate_angle'])
        img = img.rotate(angle)

    if 'blur' in request.form:
        radius = float(request.form['blur_radius'])
        img = img.filter(ImageFilter.GaussianBlur(radius))

    if 'contrast' in request.form:
        factor = float(request.form['contrast_factor'])
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(factor)

    if 'crop' in request.form:
        if 'crop_coordinates' in request.form:
            coordinates = list(map(int, request.form['crop_coordinates'].split(',')))
            img = img.crop(coordinates)

    if 'grayscale' in request.form:
        img = img.convert('L')

    if 'add_text' in request.form:
        text = request.form['text_input']
        draw = ImageDraw.Draw(img)
        font_size = 36  # Change this value to increase or decrease the font size
        draw.text((10, 10), text, fill=(255, 0, 0), font=ImageFont.truetype('arial.ttf', font_size))

    # Convert edited image to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return render_template('edit.html', img_data=img_str)

@app.route('/download')
def download():
    img_data = request.args.get('img_data')
    return send_file(img_data, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
