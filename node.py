from flask import Flask, request, jsonify
import uuid #creates the unique id
import os

#initializes flask app
app = Flask(__name__)

#generate random id
node_id = str(uuid.uuid4())

#stores known peers
peers = set()

#message with id 
@app.route('/')
def index():
    return jsonify({"message": f"Node {node_id} is running!"})

#registers the peer 
@app.route('/register', methods=['POST'])
def register_peer():
    data = request.get_json()
    peer = data.get('peer')
    if peer: 
        peers.add(peer)
        return jsonify({"status": "peer registered", "peers": list(peers)}), 200
    return jsonify({"error": "no peer provide"}), 400

@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    sender = data.get('sender')
    msg = data.get('msg')
    print(f"Received message from {sender}: {msg}")
    return jsonify({"status": "received"}), 200 

@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify({"peers": list(peers)})

#starts the app
if __name__== "__main__":
    app.run(host= "0.0.0.0", port=5000)


