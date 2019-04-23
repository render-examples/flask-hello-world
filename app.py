from flask import Flask, request
app = Flask(__name__)
import matplotlib as mpl
mpl.use('TkAgg') #due to https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python
from pathlib import Path
from fastai import *
from fastai.text import *
import os

download_models()

async def download_models():
    print('Downloading models')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3.download_file('talkhiring-models','star_interview_model.pkl','/models')
    print('Downloaded models')

@app.route('/predictor/classifySTAR', methods=['POST'])
def classifySTAR():
    input_text = request.get_json().get('text')
    learner = load_learner(PATH_TO_MODELS_DIR, 'star_interview_model.pkl')
    pred_class, pred_idx, losses = self.learner.predict(input_text)
    return { 'prediction': str(pred_class), 'confidence': float(max(to_np(losses))) }

@app.route('/ping', methods=['GET'])
def ping():
    return 'OK'