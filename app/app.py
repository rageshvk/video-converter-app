from flask import Flask, request, render_template, send_from_directory
import os
import subprocess
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/uploads'
OUTPUT_FOLDER = 'app/outputs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'video' not in request.files:
        return "No file part", 400
    file = request.files['video']
    format = request.form['format']
    if file.filename == '' or not allowed_file(file.filename):
        return "Invalid file", 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    output_filename = filename.rsplit('.', 1)[0] + f'.{format}'
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    command = ['ffmpeg', '-i', input_path, output_path]
    subprocess.run(command)

    return f'<a href="/download/{output_filename}">Download Converted File</a>'

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)