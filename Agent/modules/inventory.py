import platform, psutil, socket
import json
import subprocess
import winreg
import cpuinfo
import wmi


CPU_NAME = cpuinfo.get_cpu_info().get('brand_raw', 'Unknown') 






def get_device_type():
    return "laptop" if psutil.sensors_battery() else "desktop"



def get_installed_programs_registry():
    programs = []

    registry_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    for hive, path in registry_paths:
        try:
            reg_key = winreg.OpenKey(hive, path)
        except FileNotFoundError:
            continue

        for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
            try:
                subkey_name = winreg.EnumKey(reg_key, i)
                subkey = winreg.OpenKey(reg_key, subkey_name)
                display_name, _ = winreg.QueryValueEx(subkey, "DisplayName") if "DisplayName" in [winreg.EnumValue(subkey, j)[0] for j in range(winreg.QueryInfoKey(subkey)[1])] else (None, None)
                display_version, _ = winreg.QueryValueEx(subkey, "DisplayVersion") if "DisplayVersion" in [winreg.EnumValue(subkey, j)[0] for j in range(winreg.QueryInfoKey(subkey)[1])] else (None, None)

                if display_name:
                    programs.append({"name": display_name, "version": display_version})
            except FileNotFoundError:
                continue
            except OSError:
                continue
    return programs

def get_disks_info():
    c = wmi.WMI()
    disks_info = []

    # Listado de discos físicos para detectar SSD/HDD
    physical_disks = []
    for disk in c.Win32_DiskDrive():
        physical_disks.append({
            "device_id": disk.DeviceID,
            "model": disk.Model,
            "type": "SSD" if "SSD" in (disk.MediaType or "") else "HDD"
        })

    # Mapear particiones
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue

        # Determinar tipo de disco asociado
        disk_type = "Unknown"
        for pd in physical_disks:
            if part.device.replace("\\\\?\\", "") in pd["device_id"]:
                disk_type = pd["type"]
                break

        disks_info.append({
            "mountpoint": part.mountpoint,
            "fstype": part.fstype,
            "total_gb": usage.total // (1024**3),
            "used_gb": usage.used // (1024**3),
            "free_gb": usage.free // (1024**3),
            "percent": usage.percent,
            "type": disk_type
        })

    return disks_info

def get_gpu_info():
    # devuelve un json con la info de las gpus
    c = wmi.WMI()
    gpus = []
    for gpu in c.Win32_VideoController():
        gpus.append({
            "name": gpu.Name,
            "driver_version": gpu.DriverVersion,
            "vram_mb": int(gpu.AdapterRAM) // (1024**2)
        })
    return gpus

def get_local_ip_addresses():
    # devuelve un json con la info de las ip locales
    ip_addresses = []
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_addresses.append(addr.address)
    return ip_addresses


def get_mac_addresses():
    # devuelve un json con la info de las mac
    mac_addresses = []
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                mac_addresses.append(addr.address)
    return mac_addresses

def get_antivirus_info():
    # devuelve un json con la info de los antivirus instalados
    c = wmi.WMI(namespace="root\\SecurityCenter2")
    antiviruses = []
    for av in c.AntiVirusProduct():
        antiviruses.append({
            "name": av.displayName,
            "path": av.pathToSignedProductExe,
            "state": av.productState
        })
    return antiviruses


def check_pending_updates():
    try:
        output = subprocess.check_output(["powershell", "-Command", "Get-WindowsUpdate -IsPending"], universal_newlines=True)
        return "No pending updates found." not in output
    except subprocess.CalledProcessError:
        return False

def get_inventory_json():
    cpu = psutil.cpu_freq()
    ram = psutil.virtual_memory()
    disks = get_disks_info()
   
    
    inventory = {
        "hostname": socket.gethostname(),
        "device_type": get_device_type(),
        "os": platform.system() + " " + platform.release(),
        "cpu_name": CPU_NAME,
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "cpu_usage": psutil.cpu_percent(interval=0.5),
        "ram_total": ram.total // (1024**3),
        "ram_used": ram.used // (1024**3),
        "disk": disks,
        "ip": get_local_ip_addresses(),
        "gpu": get_gpu_info(),
        "mac": get_mac_addresses(),
        "windows_version": platform.version(),
        "windows_build": platform.win32_ver()[1],
        "anti_virus": get_antivirus_info(),
        "pending_updates": check_pending_updates(),
        "installed_programs": get_installed_programs_registry()
    }

    return inventory