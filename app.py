import os
from flask import Flask, request, jsonify, abort, make_response
from werkzeug.utils import secure_filename
# -*- coding: utf-8 -*-

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt','py'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/uploads', methods=['POST'])
def index():
    if request.method == 'POST':
        #check if the post request has the file part
        if 'file' not in request.files:
            abort(404)
        file = request.files['file']
        if file.filename is None:
            abort(404)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'filename' : filename}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'File Not Found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
