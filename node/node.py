from flask import Flask, request, jsonify
import uuid #creates the unique id
import os

#initializes flask app
app = Flask(__name__)

#generate random id
node_id = str(uuid.uuid4())

#message with id 
@app.route('/node', methods=['GET'])
def index():
    return jsonify({"Message: Node " + node_id + " is running!"})

#starts the app
if __name__== "__main__":
    app.run(host= "0.0.0.0", port=6000)


