# Peer-to-Peer
This project is a Phase 1 implementation of a Peer-to-Peer (P2P) system using Flask and Docker. The system includes a centralized Bootstrap Node that manages peer registration, while the other nodes (peers) can discover and interact with each other using HTTP.

.
├── bootstrap.Dockerfile     # Dockerfile for bootstrap server
├── bootstrap.py             # Flask server for node registration and discovery
├── Dockerfile               # Dockerfile for peer nodes
├── node.py                  # Peer node logic (registration, communication)
├── docker-compose.yml       # Multi-container orchestration (bootstrap + 12 nodes)
├── README.md                # Project documentation

1. Build and Starte the network:
```bash
docker-compose up --build
```

2. Check Running Containers: 
```bash
docker ps
```

3. Test Node Message Passing USE cure: 
```bash
curl -X POST http://localhost:5001/message \
  -H "Content-Type: application/json" \
  -d '{"sender": "NodeX", "msg": "Hello, Node1!"}'
```