

# https://auth0.com/blog/developing-restful-apis-with-python-and-flask/

from email import message
from flask import Flask, request, jsonify, redirect
import datetime
import av
import numpy as np
import logging
import argparse
import stt
import os
import urllib.request
from werkzeug.utils import secure_filename

from pkg_resources import require

#https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login-es

app = Flask(__name__)

UPLOAD_FOLDER = './upload_files'
#app.secret_key = "g00dby3m1tr0l"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

stt = stt.DeepSpeech()
stt.init_model(model_path='model/model.pbmm', scorer='model/kenlm_es.scorer', beam_width=None, lm_beta=None, lm_alpha=None)

#https://realpython.com/playing-and-recording-sound-python/
@app.route('/version/', methods=['GET'])
def get_version():
    return jsonify({'version':'1.0.0'})

ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'ogg', 'flac'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def health_check():
    return 'OK'

@app.route('/v1/deep-speech', methods=['POST'])
def upload_deepspeech():
    try:
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in request'})
            resp.status_code = 400
            return resp
        
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        
        if (not file) or (not allowed_file(file.filename)):
            resp = jsonify({'message': 'Not allowed  file extension'})
            resp.status_code = 400
            return resp
        
        channels = int(request.form['channels'])
        
        filename = secure_filename(file.filename)
        full_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        ext = filename.rsplit('.', 1)[1].lower()
        transcript = full_name.replace('.'+ext, '.txt')
        file.save(full_name)

        # CRUD MondoDB
        callid_default = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        response = stt.Recognize(full_name)

        print(u"Transcript: {}".format(response))
        with open(transcript, 'w') as f:
            f.write(str(response) + '\n')

        resp = jsonify({'message': 'file uploaded!', 'transcript': str(response)})
        resp.status_code = 200
        return resp
    except Exception as e:
        return jsonify({'error': str(e)}) 
        

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-m', '--model', required=True, help='Modelo acustico')
    #parser.add_argument('-s', '--scorer', required=False, help='Red KenLM')
    #parser.add_argument('-bw', '--beam', required=False, help='Beam Width')
    #parser.add_argument('-b', '--beta', required=False, help='Beta LM')
    #parser.add_argument('-a', '--alpha', required=False, help='Alpha LM')
    #ARGS = parser.parse_args()
    #stt.init_model(model_path=ARGS.model, scorer=ARGS.scorer, beam_width=ARGS.beam, lm_beta=ARGS.beta, lm_alpha=ARGS.alpha)
    app.run(debug=True)