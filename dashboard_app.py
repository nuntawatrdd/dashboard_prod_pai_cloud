from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "current_infra.json"

@app.route('/api/update', methods=['POST'])
def update_infra():
    req_data = request.json
    
    if req_data and "value" in req_data:
        payload = req_data["value"]
    else:
        payload = req_data if req_data else {}
        
    payload["update_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(DATA_FILE, "w") as f:
        json.dump(payload, f)
        
    return jsonify({"status": "success", "message": "Dashboard updated!"})

@app.route('/api/data', methods=['GET'])
def get_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/')
def dashboard():
    # โหลดไฟล์ index.html จากโฟลเดอร์ templates
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)