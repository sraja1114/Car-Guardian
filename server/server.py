import os
import shutil
import time
import webbrowser
import threading
from flask import Flask, jsonify, request

app = Flask(__name__)
currentSensitivity = "High"

def save_file(file_folder, file_path_collision, file_path_loud_noise, data_type, file_list_initial):
    start_time = time.time()
    for i in range(120): # monitor downloads folder for new files, timeout after 120 seconds
        file_list_new = os.listdir(file_folder)
        file_count_new = len(file_list_new)
        print(file_count_new)
        print(file_count_initial)
        if file_count_new > file_count_initial:
            time.sleep(2)
            newfile = [x for x in file_list_new if x not in file_list_initial] # get new file
            newfile = newfile[0]
            end_time = time.time()
            time_elapsed = end_time - start_time
            if time_elapsed < 15: # if within fifteen seconds of new file when it did this it should send over two
                if data_type == 'pre-collision':
                    old_path = file_folder + "/" + newfile
                    new_path = file_path_collision + "/" + newfile
                    shutil.move(old_path, new_path)
                    return jsonify({"message": "Successfully moved file due to " + data_type})
                if data_type == 'loud-noise':
                    old_path = file_folder + "/" + newfile
                    new_path = file_path_loud_noise + "/" + newfile
                    shutil.move(old_path, new_path)
                    return jsonify({"message": "Successfully moved file due to " + data_type})
                return jsonify({"message": "Could not move file due to unknown type of: " + data_type})
            else:
                print('move one')
                if data_type == 'pre-collision':
                    old_path = file_folder + "/" + newfile
                    new_path = file_path_collision + "/" + newfile
                    shutil.move(old_path, new_path)
                    return jsonify({"message": "Successfully moved file due to " + data_type})
                if data_type == 'loud-noise':
                    old_path = file_folder + "/" + newfile
                    new_path = file_path_loud_noise + "/" + newfile
                    shutil.move(old_path, new_path)
                    return jsonify({"message": "Successfully moved file due to " + data_type})
                return jsonify({"message": "Could not move file due to unknown type of: " + data_type})
        print('no new file ' + str(i))
        time.sleep(1)
    return jsonify({"message": "Successfully moved file due to " + data_type})

@app.route('/record', methods=['POST'])
def precollision():
    body_data = request.get_json()
    data_type = body_data.get('type')
    currentPath = os.path.dirname(os.path.realpath(__file__))
    file_path_loud_noise = currentPath + "/../Saved Videos/Noises"
    file_path_collision = currentPath + "/../Saved Videos/Pre-Collision"
    
    file_path = currentPath + "/../Saved Videos"
    file_folder = os.path.expanduser(file_path)
    global file_count_initial
    file_list_initial = os.listdir(file_folder)
    file_count_initial = len(file_list_initial)
    
    # Start file-saving process in a separate thread
    threading.Thread(target=save_file, args=(file_folder, file_path_collision, file_path_loud_noise, data_type, file_list_initial)).start()
    
    return jsonify({"message": "File saving process started."})

if __name__ == '__main__':
    app.run(debug=True, port=3001)
