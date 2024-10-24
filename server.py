import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
latest_message = None  

@app.route('/send', methods=['POST'])
def send_message():
    global latest_message
    data = request.get_json()
    message = data.get('message')
    if message:
        latest_message = message  
        return jsonify({"status": "Message received"}), 200
    return jsonify({"error": "Message not provided"}), 400

@app.route('/latest', methods=['GET'])
def get_latest_message():
    if latest_message is not None:
        return jsonify({"latest_message": latest_message}), 200
    return jsonify({"latest_message": "No messages yet"}), 200

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({'files': files}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({'message': f'File {file.filename} uploaded successfully'}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
