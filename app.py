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
from flask import jsonify

def download_models():
    print('Downloading models')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    if not os.path.exists('models/'):
        os.makedirs('models/')

    list_of_model_file_paths = [
        'models/star_interview_model.pkl',
        'models/concision_model.pkl'
    ]

    for model_path in list_of_model_file_paths:
        exists = os.path.isfile(model_path)
        if exists:
            print('Model already downloaded.  Not downloading')
        else:
            file_name = model_path.split('/')[1]
            s3.download_file('talkhiring-models', file_name, model_path)
    print('Downloaded models')

@app.route('/textClassifier/classifySTAR', methods=['POST'])
def classifySTARRoute():
    input_text = request.get_json().get('text')
    return jsonify(classifySTAR(input_text))

@app.route('/textClassifier/classifyConcision', methods=['POST'])
def classifyConcisionRoute():
    input_text = request.get_json().get('text')
    return jsonify(classifyConcision(input_text))

def classifyConcision(text):
    learner = load_learner('models/', 'concision_model.pkl')
    # if recordings are on the shorter side, assume that they are always concise
    # otherwise, sometimes for very short recordings, we say that they are rambling when that does not make sense
    # Harris did an analysis and found that, for recordings of 30 seconds or less, the 3rd quartile transcription length was 55
    if (text.length < 55) return { 'prediction': 'Yes', 'confidence': 1.0 }
    pred_class, pred_idx, losses = learner.predict(text)
    return { 'prediction': str(pred_class), 'confidence': float(max(to_np(losses))) }

def classifySTAR(text):
    learner = load_learner('models/', 'star_interview_model.pkl')
    pred_class, pred_idx, losses = learner.predict(text)
    return { 'prediction': str(pred_class), 'confidence': float(max(to_np(losses))) }

@app.route('/ping', methods=['GET'])
def ping():
    result = classifySTAR('ricky bobby')
    if result['prediction'] == 'Yes' or result['prediction'] == 'No':
        pass
    else:
        print('Ping result', result)
        return abort(500)

    result = classifyConcision('ricky bobby')
    if result['prediction'] == 'Yes' or result['prediction'] == 'No':
        return 'OK'
    else:
        print('Ping result', result)
        return abort(500)
        
download_models()
