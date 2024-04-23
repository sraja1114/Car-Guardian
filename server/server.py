from flask import Flask, jsonify, request
import os
import webbrowser
import datetime, time

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

@app.route('/record', methods=['POST'])
def precollision():
    body_data = request.get_json()
    data_type = body_data.get('type')
    
    downloads_folder = os.path.expanduser("~/Downloads")
    downloads_list = os.listdir(downloads_folder)
    downloads_count_initial = len(downloads_list)
    start_time = datetime.now()
    
    
    
    for i in range(120): #monitorp downloads folder for new files, timeout after 120 seconds
        downloads_list = os.listdir(downloads_folder)
        downloads_count_new = len(downloads_list)
        new_files = [f for f in downloads_count_new if f not in downloads_count_initial]
        if new_files:
            
            new_file_name = new_files[0] # new file added in the meantime - should be newly saved file
            print(new_file_name)
            break
            
        time.sleep(1)
    
    
    return jsonify({"message": "Successfully moved file due to " + data_type})


if __name__ == '__main__':
    app.run(debug=True, port=3001) 