from flask import Flask, request, jsonify

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

