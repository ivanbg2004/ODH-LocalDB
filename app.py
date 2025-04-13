from flask import Flask, request, jsonify
from odh_local_storage import ODHLocalStorage

app = Flask(__name__)
db = ODHLocalStorage("odh_storage.db")

@app.route('/set_data', methods=['POST'])
def set_data():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    db.set_item(key, value)
    return jsonify({'message': 'Data set successfully'})

@app.route('/get_data', methods=['GET'])
def get_data():
    key = request.args.get('key')
    value = db.get_item(key)
    if value:
        return jsonify({'value': value})
    else:
        return jsonify({'value': None, 'message': 'Key not found'})

@app.route('/clear_data', methods=['POST'])
def clear_data():
    db.clear()
    return jsonify({'message': 'Data cleared successfully'})

if __name__ == '__main__':
    app.run(debug=True)
