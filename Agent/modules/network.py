from pocketbase import PocketBase
from config import PB_URL, AGENT_TOKEN, AGENT_ID
import requests


pb_client = PocketBase(PB_URL)



HEADERS = {
    "Authorization": f"Bearer {AGENT_TOKEN}",
    "Content-Type": "application/json"
}


def send_inventory(agent_id, inventory: dict):
    url = f"{PB_URL}/api/collections/agents/records/{agent_id}"
    try:
        resp = requests.patch(url, json=inventory, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.status_code, resp.json()
    except requests.exceptions.RequestException as e:
        return 0, str(e)
    

def fetch_tasks(agent_id: str):
    """
    Recupera las tareas pendientes para este agente desde PocketBase.
    """
    try:
        result = pb_client.collection("tasks").get_list(
            1, 20,
            {"filter": f"agent_id = '{agent_id}' && status = 'pending'"}
        )
        items = result.items
        print(f"Fetched {len(items)} pending tasks for agent {agent_id}")
        return items
    except Exception as e:
        print("Error fetching tasks:", e)
        return []
    
def update_task_status(task_id, status):
    """
    Actualiza el estado de una tarea en el servidor.
    """
    url = f"{PB_URL}/api/collections/tasks/records/{task_id}"
    payload = {
        "status": status
    }
    try:
        resp = requests.patch(url, json=payload, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.status_code, resp.json()
    except requests.exceptions.RequestException as e:
        return 0, str(e)
    
def send_log(task_id, message, status):
    """
    Envía el resultado de una tarea al servidor.
    """
    url = f"{PB_URL}/api/collections/tasks/records/{task_id}"
    payload = {
        "log": message,
        "status": status
    }
    try:
        resp = requests.patch(url, json=payload, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.status_code, resp.json()
    except requests.exceptions.RequestException as e:
        return 0, str(e)