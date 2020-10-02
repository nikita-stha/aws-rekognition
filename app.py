import os
import json
from flask import Flask
from dotenv import load_dotenv
from urllib.parse import urlparse
from flask import render_template, request, redirect, url_for

from utils import s3, detect_face, celebrity

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

S3_BUCKET_URL = 'https://{}.s3.us-east-1.amazonaws.com/'.format(os.getenv('S3_BUCKET'))


app = Flask(__name__)
app.config['S3_BUCKET'] = os.getenv('S3_BUCKET')
app.config['S3_BUCKET_URL'] = S3_BUCKET_URL
app.config['AWS_CREDENTIALS'] = {
 "aws_access_key_id": os.getenv('AWS_ACCESS_KEY'),
"aws_secret_access_key": os.getenv('AWS_SECRET_ACCESS_KEY'),
"aws_session_token":os.getenv('AWS_SESSION_TOKEN')
}

@app.route("/")
def main():
    return render_template('index.html', response = None)

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['image_file']
    if uploaded_file.filename != '':
        response = s3.upload(uploaded_file, app.config['S3_BUCKET'], app.config['AWS_CREDENTIALS'])

        if response:
            response = {"message":"File successfully uploaded to S3", "s3_url":"{}{}".format(app.config['S3_BUCKET_URL'], response['data'])}
        else:
            response =  {"error":"Failed to upload file"}
    return render_template('index.html', response = response)

@app.route('/analyse', methods=['GET'])
def analyse_face():
    image_s3_url = request.args.get('img_s3_url')
    if image_s3_url:
        file_name = os.path.basename(urlparse(image_s3_url).path)
        face_features = detect_face.detect_faces_s3(file_name, app.config['S3_BUCKET'], app.config['AWS_CREDENTIALS'])
        if face_features is None:
            response = {"error":"No Face Detected", "data":None}
            
            return response
        face_analysed = detect_face.analyse_face(face_features)
        response = {"message":"Face analysis success", "data":face_analysed}
    return response

@app.route('/detect-celebrity', methods=['GET'])
def detect_celebrity():
    image_s3_url = request.args.get('img_s3_url')
    if image_s3_url:
        file_name = os.path.basename(urlparse(image_s3_url).path)
        data = celebrity.recogize(file_name, app.config['S3_BUCKET'], app.config['AWS_CREDENTIALS'])
        if data is None:
            response = {"error":"No any celebrities detected in the given image", "data":None}
            
            return response
        response = {"message":"Celebrities detected", "data":data}
    return response

if __name__ == "__main__":
    app.run(debug=os.getenv('DEBUG'))