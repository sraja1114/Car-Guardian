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
        
if __name__ == '__main__':
    app.run(debug=True, port=3001) 
