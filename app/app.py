# app/app.py

import os
import sys
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Add project root to sys.path to import main
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import process_video

UPLOAD_FOLDER = 'app/static/uploads'
PROCESSED_FOLDER = 'app/static/processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files['video']
        if video:
            filename = secure_filename(video.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], 'labeled_' + filename)

            video.save(input_path)
            process_video(input_path, output_path)

            return render_template('index.html', processed_video='labeled_' + filename)

    return render_template('index.html', processed_video=None)

if __name__ == '__main__':
    app.run(debug=True)
