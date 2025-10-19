import subprocess
import os
import socket
import threading
import time
from queue import Queue
from .network import update_task_status
# Cola de tareas internas para ejecución en threads
task_queue = Queue()

# -------------------------------
# Función principal para ejecutar tarea
# -------------------------------
def execute_task(task):
    """
    Ejecuta una tarea y devuelve un diccionario con resultado.
    Si la tarea es larga o interactiva, se ejecuta en un thread.
    """
    print("Ejecutando tarea:", task)
    # Manejar tanto diccionarios como objetos Record
    if hasattr(task, 'type'):
        action = task.type
        params = getattr(task, 'params', {})
    else:
        action = task.get("type")
        params = task.get("params", {})
    print("Acción:", action)


    # Definir tareas que se pueden ejecutar en threads
    threaded_actions = ["script", "deploy", "wol", "remote", "file", "patch"]

    if action in threaded_actions:
        thread = threading.Thread(target=_task_worker, args=(task,))
        thread.start()
        return {"status": "queued", "message": f"Tarea {action} en ejecución en background"}
    else:
        # tareas cortas / instantáneas
        return _task_worker(task)

# -------------------------------
# Worker real de ejecución
# -------------------------------
def _task_worker(task):
    # Manejar tanto diccionarios como objetos Record
    if hasattr(task, 'type'):
        action = task.type
        command = getattr(task, 'command', None)
        params = getattr(task, 'params', {})
    else:
        action = task.get("type")
        command = task.get("command")
        params = task.get("params", {})

    print(f"Worker ejecutando acción: {action} con command: {command} y params: {params}")
    try:
        if action == "script":
            if command:
                return run_script(task)
            elif params and isinstance(params, dict) and "script" in params:
                return run_script(params["script"])
            else:
                return {"status": "error", "message": "No se proporcionó script ni command"}
        elif action == "deploy":
            return deploy_app(params)
        elif action == "wol":
            return wake_on_lan(params)
        elif action == "remote":
            return open_console(params)
        else:
            return {"status": "error", "message": f"Acción desconocida: {action}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------------------
# Funciones por tipo de tarea
# -------------------------------
def run_script(task):
    """
    Ejecuta un comando en el sistema. 
    `command` puede ser un string directo (ej: 'echo "hola mundo"').
    """
    if hasattr(task, 'command'):
        command = task.command
        task_id = task.id
    else:
        command = task.get("command")
        task_id = task.get("id")
        
    print("Ejecutando commando:", command)
    if not command:
        return {"status": "error", "message": "No se proporcionó comando"}
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        update_task_status(task_id, "done")
        print("Comando ejecutado con éxito:", result.stdout)
    return {
        "status": "success" if result.returncode == 0 else "error",
        "message": result.stdout + result.stderr
    }

def deploy_app(params):
    path = params.get("path")
    if not path or not os.path.exists(path):
        return {"status": "error", "message": "Archivo no encontrado"}
    # MSI o EXE silencioso
    cmd = f'msiexec /i "{path}" /quiet /norestart' if path.lower().endswith(".msi") else f'"{path}" /silent'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {
        "status": "success" if result.returncode == 0 else "error",
        "message": result.stdout + result.stderr
    }

def wake_on_lan(params):
    mac = params.get("mac")
    if not mac:
        return {"status": "error", "message": "No se proporcionó MAC"}
    mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
    packet = b'\xff' * 6 + mac_bytes * 16
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(packet, ('<broadcast>', 9))
    return {"status": "success", "message": f"WOL enviado a {mac}"}

def open_console(params):
    # Por ahora abrir CMD local
    subprocess.Popen("cmd.exe")
    return {"status": "success", "message": "Consola abierta"}

# -------------------------------
# Cola de tareas opcional para procesarlas en background
# -------------------------------
def add_task_to_queue(task):
    task_queue.put(task)

def process_queue():
    while True:
        task = task_queue.get()
        if task is None:
            break
        result = execute_task(task)
        print(f"Tarea procesada desde queue: {result}")
        task_queue.task_done()

def start_queue_processor():
    thread = threading.Thread(target=process_queue, daemon=True)
    thread.start()
