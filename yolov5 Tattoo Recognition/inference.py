import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import subprocess
import imagehash
from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
counter = 5
# Define absolute path for uploads and detected folders
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DETECTED_FOLDER = os.path.join(BASE_DIR, 'detected')
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DETECTED_FOLDER'] = DETECTED_FOLDER

class DuplicateRemover:
    def __init__(self, dirname, hash_size=8):
        self.dirname = dirname+"5"
        self.hash_size = hash_size

    def _generate_hash(self, filename):
        with Image.open(filename) as img:
            img = img.resize((128, 128), Image.Resampling.LANCZOS)
            return imagehash.average_hash(img, self.hash_size), filename
    
    def find_similar(self, similarity=80):
        fnames = [os.path.join(self.dirname, f) for f in os.listdir(self.dirname) if not f.startswith('.')]
        threshold = 1 - similarity / 100
        diff_limit = int(threshold * (self.hash_size ** 2))
        hashes = {}
        unique_similars = set()

        with ThreadPoolExecutor() as executor:
            for img_hash, filename in executor.map(self._generate_hash, fnames):
                hashes[filename] = img_hash

        for base_fname, base_hash in hashes.items():
            for compare_fname, compare_hash in hashes.items():
                if base_fname != compare_fname and np.count_nonzero(base_hash.hash != compare_hash.hash) <= diff_limit:
                    unique_similars.add(compare_fname)

        for fname in unique_similars:
            os.remove(fname)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_video(video_path):
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed.mp4')
    command = f"ffmpeg -i {video_path} -vf mpdecimate,setpts=N/FRAME_RATE/TB -c:v libx264 -crf 30 {output_path}"
    subprocess.run(command, shell=True)
    return output_path

def detect_tattoo(video_path):
    output_dir = os.path.join(app.config['DETECTED_FOLDER'])
    command = f"python detect.py --img 720 --conf 0.30 --device 0 --weights best.pt --source {video_path} --save-txt --save-conf --save-crop --save-csv --project {output_dir}"
    subprocess.run(command, shell=True)
    return output_dir

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            compressed_path = compress_video(file_path)
            #add results save path
            output_dir = detect_tattoo(compressed_path)
            remover = DuplicateRemover(output_dir)
            remover.find_similar()
            return redirect(url_for('uploaded_file', filename=compressed_path))
    return '''
    <title>Upload new video</title>
    <h1>Upload new video</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/detected/<path:filename>')
def detected_file(filename):
    return send_from_directory(app.config['DETECTED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
