from flask import Flask, jsonify, request

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

@app.route('/sensitivity', methods=['POST'])
def sensitivity():
    data = request.get_json()
    print(data["sensitivity"])
    with open("/Users/jasonsze/Desktop/CSCE 483/repo/YOLOv4-distance-tracking/sensitivity.txt", "w") as file:
        file.write(data["sensitivity"])
    return jsonify({'message': f'{data["sensitivity"]}'})
        
if __name__ == '__main__':
    app.run(debug=True, port=3001) 
