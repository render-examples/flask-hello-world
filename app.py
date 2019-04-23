from flask import Flask, request
app = Flask(__name__)
import matplotlib as mpl
mpl.use('TkAgg') #due to https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python
from pathlib import Path
from fastai import *
from fastai.text import *
import os
import boto3
from flask import abort

def download_models():
    print('Downloading models')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    if not os.path.exists('models/'):
        os.makedirs('models/')
    
    s3.download_file('talkhiring-models','star_interview_model.pkl','models/star_interview_model.pkl')
    print('Downloaded models')

@app.route('/textClassifier/classifySTAR', methods=['POST'])
def classifySTARRoute():
    input_text = request.get_json().get('text')
    return classifySTAR(input_text)

def classifySTAR(text):
    learner = load_learner('models/', 'star_interview_model.pkl')
    pred_class, pred_idx, losses = learner.predict(text)
    return { 'prediction': str(pred_class), 'confidence': float(max(to_np(losses))) }

@app.route('/ping', methods=['GET'])
def ping():
    result = classifySTAR('ricky bobby')
    if result['prediction'] == 'Yes' or result['prediction'] == 'No':
        return 'OK'
    else:
        print('Ping result', result)
        return abort(500)
        
download_models()