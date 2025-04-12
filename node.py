from flask import Flask, request, jsonify
import uuid #creates the unique id
import requests
import time
import os
import threading

PORT = int(os.environ.get("PORT", 5000))
BOOTSTRAP_URL = os.environ.get("BOOTSTRAP", "http://localhost:5000")
 
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

def register_with_bootstrap(): 
    try: 
        peer_url = f"http://localhost:{PORT}"
        res = requests.post(f"{BOOTSTRAP_URL}/register", json={"peer": peer_url})
        if res.status_code == 200: 
            new_peers = res.json().get("peers", [])
            peers.update(new_peers)
            peers.discard(peer_url) #Removes port if already exists 
            print(f"[Node {node_id}] Discovered peers: {peers}")
    except Exception as e: 
        print(f"Error registering with bootstrap: {e}")

threading.Thread(target=register_with_bootstrap).start()

app.run(host='0.0.0.0', port=PORT)
#starts the app
if __name__== "__main__":
    app.run(host= "0.0.0.0", port=5000)


