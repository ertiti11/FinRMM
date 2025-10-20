# Agent/modules/autoupdate.py

import requests
import subprocess
import os
import sys
import hashlib
import tempfile
from pathlib import Path
from config import PB_URL, AGENT_TOKEN, CURRENT_VERSION

HEADERS = {
    "Authorization": f"Bearer {AGENT_TOKEN}",
    "Content-Type": "application/json"
}

UPDATE_CHECK_URL = f"{PB_URL}/api/collections/agent_updates/records"

def get_file_hash(filepath):
    """Calcula el hash SHA256 de un archivo"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_for_updates():
    """
    Verifica si hay actualizaciones disponibles en PocketBase
    Busca registros en la colección 'agent_updates' con versión mayor a la actual
    """
    try:
        # Buscar actualizaciones disponibles
        params = {
            "filter": f"status = 'available'",
            "sort": "-version"
        }
        resp = requests.get(UPDATE_CHECK_URL, headers=HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        
        updates = resp.json().get("items", [])
        
        if not updates:
            print("No hay actualizaciones disponibles")
            return None
        
        # Comparar versiones (simplificado, asume formato X.Y.Z)
        latest_update = updates[0]
        latest_version = latest_update.get("version")
        
        if compare_versions(latest_version, CURRENT_VERSION) > 0:
            print(f"Nueva versión disponible: {latest_version} (actual: {CURRENT_VERSION})")
            return latest_update
        else:
            print(f"Versión actual {CURRENT_VERSION} está actualizada")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error al verificar actualizaciones: {e}")
        return None

def compare_versions(v1, v2):
    """
    Compara dos versiones en formato X.Y.Z
    Retorna: 1 si v1 > v2, -1 si v1 < v2, 0 si son iguales
    """
    parts1 = [int(x) for x in v1.split('.')]
    parts2 = [int(x) for x in v2.split('.')]
    
    for i in range(max(len(parts1), len(parts2))):
        p1 = parts1[i] if i < len(parts1) else 0
        p2 = parts2[i] if i < len(parts2) else 0
        
        if p1 > p2:
            return 1
        elif p1 < p2:
            return -1
    
    return 0

def download_update(update_info):
    """
    Descarga el archivo de actualización desde PocketBase
    """
    try:
        record_id = update_info.get("id")
        installer_filename = update_info.get("installer")
        expected_hash = update_info.get("file_hash")
        
        if not installer_filename:
            print("Error: No se encontró archivo instalador en el registro")
            return None
        
        # Construir URL del archivo en PocketBase
        # Formato: {PB_URL}/api/files/{collectionId}/{recordId}/{filename}
        collection_id = update_info.get("collectionId", "agent_updates")
        file_url = f"{PB_URL}/api/files/{collection_id}/{record_id}/{installer_filename}"
        
        print(f"Descargando actualización desde: {file_url}")
        
        # Descargar archivo
        resp = requests.get(file_url, headers=HEADERS, stream=True, timeout=120)
        resp.raise_for_status()
        
        # Guardar en archivo temporal
        file_extension = os.path.splitext(installer_filename)[1]
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
        
        total_size = int(resp.headers.get('content-length', 0))
        downloaded = 0
        
        with open(temp_file.name, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    print(f"Descargando... {progress:.1f}%", end='\r')
        
        print("\nDescarga completada")
        
        # Verificar hash si está disponible
        if expected_hash:
            print("Verificando integridad del archivo...")
            file_hash = get_file_hash(temp_file.name)
            if file_hash != expected_hash:
                print("Error: Hash del archivo no coincide")
                print(f"Esperado: {expected_hash}")
                print(f"Obtenido: {file_hash}")
                os.unlink(temp_file.name)
                return None
            print("✅ Hash verificado correctamente")
        
        print(f"Actualización descargada en: {temp_file.name}")
        return temp_file.name
        
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar actualización: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def apply_update(update_file):
    """
    Aplica la actualización ejecutando el instalador
    """
    try:
        print("Aplicando actualización...")
        
        # Determinar el tipo de instalador y comando apropiado
        if update_file.lower().endswith('.msi'):
            install_cmd = f'msiexec /i "{update_file}" /quiet /norestart'
        else:
            install_cmd = f'"{update_file}" /silent /norestart'
        
        # Crear script batch para actualizar y reiniciar
        batch_content = f"""@echo off
echo Esperando cierre del agente...
timeout /t 3 /nobreak >nul
echo Instalando actualización...
{install_cmd}
timeout /t 5 /nobreak >nul
echo Limpiando archivos temporales...
del "{update_file}"
echo Reiniciando agente...
cd /d "{os.path.dirname(sys.executable)}"
start "" "{sys.executable}" "{sys.argv[0]}"
del "%~f0"
"""
        
        batch_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.bat')
        batch_file.write(batch_content)
        batch_file.close()
        
        print(f"Script de actualización creado: {batch_file.name}")
        
        # Ejecutar batch y cerrar agente
        subprocess.Popen(['cmd', '/c', batch_file.name], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.DETACHED_PROCESS)
        
        print("=" * 50)
        print("Actualización iniciada.")
        print("El agente se cerrará y reiniciará automáticamente.")
        print("=" * 50)
        
        # Dar tiempo al batch para iniciar
        import time
        time.sleep(2)
        
        # Cerrar el agente actual
        sys.exit(0)
        
    except Exception as e:
        print(f"Error al aplicar actualización: {e}")
        return False

def auto_update():
    """
    Función principal de autoupdate
    Verifica, descarga e instala actualizaciones automáticamente
    """
    print("\n" + "=" * 50)
    print("VERIFICANDO ACTUALIZACIONES...")
    print("=" * 50)
    
    update_info = check_for_updates()
    
    if not update_info:
        return False
    
    # Verificar si la actualización debe aplicarse automáticamente
    auto_install = update_info.get("auto_install", True)
    
    if not auto_install:
        print("⚠️  Actualización disponible pero auto_install está deshabilitado")
        print(f"   Versión: {update_info.get('version')}")
        print(f"   Notas: {update_info.get('release_notes', 'N/A')}")
        return False
    
    print(f"\n📦 Nueva actualización encontrada:")
    print(f"   Versión: {update_info.get('version')}")
    print(f"   Tamaño: {update_info.get('size_mb', 'N/A')} MB")
    print(f"   Notas: {update_info.get('release_notes', 'N/A')[:100]}")
    
    # Descargar actualización
    update_file = download_update(update_info)
    
    if not update_file:
        print("❌ Error al descargar la actualización")
        return False
    
    # Aplicar actualización
    apply_update(update_file)
    
    return True

def manual_update_check():
    """
    Función para verificación manual que retorna información sin aplicar
    """
    update_info = check_for_updates()
    
    if update_info:
        return {
            "update_available": True,
            "version": update_info.get("version"),
            "release_notes": update_info.get("release_notes"),
            "size_mb": update_info.get("size_mb"),
            "auto_install": update_info.get("auto_install", False)
        }
    else:
        return {
            "update_available": False,
            "current_version": CURRENT_VERSION
        }