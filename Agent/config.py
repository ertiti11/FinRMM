# agent/config.py
import os
PB_URL = "http://localhost:8090"
PB_API_URL = "http://localhost:8090/api"
AGENT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2xsZWN0aW9uSWQiOiJfcGJfdXNlcnNfYXV0aF8iLCJleHAiOjE3OTIyODk2NzUsImlkIjoiZXVpazJ0dnd0cG44NzBlIiwicmVmcmVzaGFibGUiOmZhbHNlLCJ0eXBlIjoiYXV0aCJ9.hLvqsoEDPb0ucn5HPVx3FZsSgKDLQ-tWkD1LM2GARlA"
AGENT_ID = "agent-uuid-1234"
INVENTORY_INTERVAL = 5  # segundos entre reportes de inventario
TASK_INTERVAL = 60     # segundos entre chequeo de tareas
USER = os.getlogin()
DB_FILE = f"C:\\Users\\{USER}\\AppData\\Local\\Temp\\RMM.db"


# Configuración de autoupdate
AUTO_UPDATE_ENABLED = True  # Habilitar/deshabilitar autoupdate
CURRENT_VERSION = "1.0.0"  # Versión actual del agente