from modules import init_agent, inventory, network, tasks
from config import INVENTORY_INTERVAL, TASK_INTERVAL
import time

def main_loop():
    print("Iniciando agente RMM...")

    agent_id = init_agent.register_agent()
    if not agent_id:
        print("No se pudo inicializar el agente. Saliendo...")
        return

    last_inventory = 0
    last_tasks = 0

    while True:
        now = time.time()

        if now - last_inventory > INVENTORY_INTERVAL:
            inv = inventory.get_inventory_json()
            network.send_inventory(agent_id, inv)
            last_inventory = now

        if now - last_tasks > TASK_INTERVAL:
            tasks_list = network.fetch_tasks(agent_id)
            for t in tasks_list:
                result = tasks.execute_task(t)
                network.send_log(t.id, result['message'], result['status'])
            last_tasks = now

        time.sleep(1)
if __name__ == "__main__":
    main_loop()
