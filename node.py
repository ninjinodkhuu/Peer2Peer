import threading
import time
import requests
import uuid
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Unique ID and peer list
node_id = str(uuid.uuid4())[:8]  # Shortened for clearer logs
peers = set()
bootstrap_url = "http://bootstrap:5000"  # Use container name within Docker network


@app.route('/register', methods=['POST'])
def register_peer():
    data = request.get_json()
    peer_url = data.get("peer")
    if peer_url and peer_url != request.host_url.strip('/'):
        peers.add(peer_url)
        print(f"[{node_id}] Registered new peer: {peer_url}")
        return jsonify({"status": "peer registered", "peers": list(peers)})
    return jsonify({"status": "failed", "reason": "invalid peer"}), 400


@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify(list(peers))


@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    sender = data.get('sender')
    msg = data.get("msg")

    
    print(f"[{datetime.now().strftime('%I:%M:%S %p')}] Message received from {sender}: {msg}", flush=True)


    return jsonify({"status": "message received"}), 200


def register_with_bootstrap():
    time.sleep(2)  # Let Flask fully start
    try:
        my_url = f"http://{get_container_ip()}:5000"
        res = requests.post(f"{bootstrap_url}/register", json={"peer": my_url})
        if res.ok:
            print(f"[{node_id}] Registered with bootstrap. My URL: {my_url}")
            peers.update(res.json().get("peers", []))
        else:
            print(f"[{node_id}] Failed to register. Response: {res.status_code}")
    except Exception as e:
        print(f"[{node_id}] Error registering with bootstrap: {e}")


def get_container_ip():
    import socket
    return socket.gethostbyname(socket.gethostname())


def update_peers():
    while True:
        current_peers = list(peers)
        for peer in current_peers:
            try:
                res = requests.get(f"{peer}/peers", timeout=3)
                if res.ok:
                    new_peers = set(res.json())
                    if new_peers - peers:
                        print(f"[{node_id}] New peers discovered: {new_peers - peers}")
                    peers.update(new_peers)
            except Exception as e:
                print(f"[{node_id}] Failed to contact {peer}: {e}")
        time.sleep(10)


if __name__ == '__main__':
    print(f" Node starting up with ID: {node_id}")
    threading.Thread(target=register_with_bootstrap).start()
    threading.Thread(target=update_peers).start()
    app.run(host='0.0.0.0', port=5000)
