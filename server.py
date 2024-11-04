import os
import threading
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
latest_message = None  
logged_in={}


USER_DATA_FILE = 'users.txt'

def add_user(username, password):
    if user_exists(username):
        return False
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username}:{password}\n")
    return True

def user_exists(username):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                stored_username = line.split(':')[0]
                if stored_username == username:
                    return True
    return False

def verify_user(username, password):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split(':')
                if stored_username == username and stored_password == password:
                    return True
    return False

@app.route('/check_login', methods=['GET'])
def check_login():
    usernamee = request.args.get('username')
    
    if usernamee in logged_in:
        return jsonify({"status": "user verified"}), 200
    return jsonify({"error": "login in first"}), 401


@app.route('/send', methods=['POST'])
def send_message():
    global latest_message
    data = request.get_json()
    message = data.get('message')
    if message:
        latest_message = message  
        username = message.split(':')[0]  
        if username in logged_in:
            logged_in[username]['last_active'] = time.time()  
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




@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if verify_user(username, password):
            logged_in[username] = {'username': username, 'last_active': time.time()} 
            app.logger.info(f"User {username} logged in.")
            return jsonify({"status": "Login successful"}), 200


    except Exception as e:
        app.logger.error(f"Error in login: {e}")
        return jsonify({"error": "An error occurred during login."}), 500


@app.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    

    if add_user(username, password):
        return jsonify({"status": "User  registration successful"}), 200
    return jsonify({"error": "User  already exists, please login"}), 401

def cleanup_inactive_users():
    while True:
        time.sleep(60) 
        current_time = time.time()
        to_remove = []

        for username, data in logged_in.items():
            if current_time - data['last_active'] > 15 * 60:  
                to_remove.append(username)

        
        for username in to_remove:
            del logged_in[username]
            app.logger.info(f"User {username} has been removed due to inactivity.")

threading.Thread(target=cleanup_inactive_users, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)
