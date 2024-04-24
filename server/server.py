import os
import shutil
import time
import webbrowser

from flask import Flask, jsonify, request

app = Flask(__name__)
currentSensitivity = "High"

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

@app.route('/sensitivity', methods=['POST'])
def sensitivity():
    data = request.get_json()
    global currentSensitivity
    currentSensitivity = data["sensitivity"]
    output = jsonify({'message': f'{data["sensitivity"]}'})
    print(output)
    return output

@app.route('/sensitivity', methods=['GET'])
def getSensitivity():
    global currentSensitivity
    return jsonify({'sensitivity': f'{currentSensitivity}'})
        
@app.route('/open_file_explorer', methods=['POST'])
def open():
    print("running")
    currentPath = os.path.dirname(os.path.realpath(__file__))
    downloads_folder = os.path.expanduser(currentPath + "/../Saved Videos")
    
    webbrowser.open_new_tab(downloads_folder)
    return jsonify({"message": "Opened downloads folder"})

@app.route('/record', methods=['POST'])
def precollision():
    body_data = request.get_json()
    data_type = body_data.get('type')
    file_path_collision = "/mnt/c/Users/james/Downloads/Saved-PreCollisions"
    
    file_path = "/mnt/c/Users/james/Downloads"
    file_folder = os.path.expanduser(file_path)
    file_list_initial = os.listdir(file_folder)
    file_count_initial = len(file_list_initial)
    start_time = time.time()
    
    for i in range(120): #monitor downloads folder for new files, timeout after 120 seconds
        file_list_new = os.listdir(file_folder)
        file_count_new = len(file_list_new)
        print(file_count_new)
        print(file_count_initial)
        if file_count_new > file_count_initial:
            newfile = [x for x in file_list_new if x not in file_list_initial] # get new file
            newfile = newfile[0]
            end_time = time.time()
            time_elapsed = end_time - start_time
            if time_elapsed < 5: #if within fifteen seconds of new file when it did this it should send over two
                print('move two')
                break #temp break
            else:
                print('move one')
                old_path = file_path + "/" + newfile
                new_path = file_path_collision + "/" + newfile
                shutil.move(old_path, new_path)
                return jsonify({"message": "Successfully moved file due to " + data_type})
            break
        print('no new file ' + str(i))
        time.sleep(1)
    
    
    return jsonify({"message": "Successfully moved file due to " + data_type})


if __name__ == '__main__':
    app.run(debug=True, port=3001) 
