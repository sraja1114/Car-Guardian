from flask import Flask, jsonify, request
import os
import webbrowser

app = Flask(__name__)

# example get request
@app.route('/default_greet')
def hello():
    return jsonify({"message": "Hello, World!"})

# example of sending a post request with data as a json
@app.route('/greet', methods=['POST'])
def greet():
    data = request.get_json()

    if 'name' in data:
        return jsonify({'message': f'Hello, {data["name"]}!'})
    else:
        return jsonify({'error': 'Missing "name" parameter'}), 400

@app.route('/open_file_explorer', methods=['GET'])
def open():
    downloads_folder = os.path.expanduser("~/Downloads")
    
    webbrowser.open_new_tab(downloads_folder)
    return jsonify({"message": "Opened downloads folder"})


if __name__ == '__main__':
    app.run(debug=True, port=3001) 