from modules import init_agent, inventory, network, tasks, autoupdate
from config import INVENTORY_INTERVAL, TASK_INTERVAL, UPDATE_CHECK_INTERVAL, AUTO_UPDATE_ENABLED
import time

def main_loop():
    print("Iniciando agente RMM...")

    agent_id = init_agent.register_agent()
    if not agent_id:
        print("No se pudo inicializar el agente. Saliendo...")
        return

    last_inventory = 0
    last_tasks = 0
    last_update_check = 0

    while True:
        now = time.time()

        # Verificar actualizaciones
        if AUTO_UPDATE_ENABLED and (now - last_update_check > UPDATE_CHECK_INTERVAL):
            print("Verificando actualizaciones...")
            try:
                autoupdate.auto_update()  # Si encuentra actualización, el agente se reiniciará
            except Exception as e:
                print(f"Error en autoupdate: {e}")
            last_update_check = now

        # Enviar inventario
        if now - last_inventory > INVENTORY_INTERVAL:
            inv = inventory.get_inventory_json()
            network.send_inventory(agent_id, inv)
            last_inventory = now

        # Ejecutar tareas
        if now - last_tasks > TASK_INTERVAL:
            tasks_list = network.fetch_tasks(agent_id)
            for t in tasks_list:
                result = tasks.execute_task(t)
                network.send_log(t.id, result['message'], result['status'])
            last_tasks = now

        time.sleep(1)

if __name__ == "__main__":
    main_loop()