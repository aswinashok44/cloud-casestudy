from app import app
import os
import time
from flask import render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'cloud-casestudy/app/static/images/'

ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/mnt/d/cloud-casestudy/vision api-61625b706645.json"

def detect_landmarks(path):
    """Detects landmarks in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude {}'.format(lat_lng.latitude))
            print('Longitude {}'.format(lat_lng.longitude))

    return landmarks

@app.route('/') 
def upload():  
    return render_template('file_upload_form.html')  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        if f.filename=='':
        	return render_template('file_upload_form.html',error="No File selected")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            absolute_path = os.path.abspath("../"+app.config['UPLOAD_FOLDER']+str(time.time()))
            f.save(absolute_path)
            landmks=detect_landmarks(absolute_path)
            return render_template("success.html", landmarks=landmks)
        return render_template('file_upload_form.html',error="File is not an image")