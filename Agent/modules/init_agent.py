import requests
import socket
import sqlite3
from config import PB_URL, AGENT_TOKEN, DB_FILE

HEADERS = {
    "Authorization": f"Bearer {AGENT_TOKEN}",
    "Content-Type": "application/json"
}

# ---- Funciones de DB ----
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS agent (
            local_id TEXT PRIMARY KEY,
            pb_id TEXT
        )
    """)
    conn.commit()
    return conn

def get_agent_record(conn):
    c = conn.cursor()
    c.execute("SELECT local_id, pb_id FROM agent LIMIT 1")
    row = c.fetchone()
    return row if row else None

def save_agent_record(conn, local_id, pb_id):
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO agent (local_id, pb_id) VALUES (?, ?)", (local_id, pb_id))
    conn.commit()

# ---- Función principal ----
def register_agent():
    conn = init_db()
    record = get_agent_record(conn)

    # Determinar local_id
    if record:
        local_id, pb_id = record
        print(f"Usando agente local: {local_id} (PB_ID: {pb_id})")
    else:
        local_id = socket.gethostname()  # o generar UUID
        pb_id = None
        print(f"No hay registro local. Usando: {local_id}")

    # Verificar si existe en PocketBase
    if pb_id:
        url = f"{PB_URL}/api/collections/agents/records/{pb_id}"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            print("Agente ya registrado en PocketBase.")
            conn.close()
            return pb_id
        else:
            print("No se encuentra PB_ID, se intentará crear de nuevo.")

    # Crear registro en PocketBase
    payload = {
        "hostname": socket.gethostname(),
        "status": "online"
    }
    create_url = f"{PB_URL}/api/collections/agents/records"
    try:
        resp = requests.post(create_url, headers=HEADERS, json=payload, timeout=10)
        resp.raise_for_status()
        pb_id = resp.json()["id"]  # Guardamos el ID que devuelve PB
        print(f"Agente registrado correctamente con PB_ID: {pb_id}")
        save_agent_record(conn, local_id, pb_id)
        conn.close()
        return pb_id
    except requests.exceptions.RequestException as e:
        print("Error al crear agente:", e)
        conn.close()
        return None
