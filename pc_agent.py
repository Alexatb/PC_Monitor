
import psutil
import platform
import socket
import requests
import time


RENDER_URL = "https://pc-monitor-azw2.onrender.com"


def get_pc_status():

    # RAM
    memory = psutil.virtual_memory()

    # Disk
    disk = psutil.disk_usage("/")

    # CPU
    cpu = psutil.cpu_percent(interval=1)

    # CPU information
    physical_cores = psutil.cpu_count(logical=False)
    logical_processors = psutil.cpu_count(logical=True)

    # CPU model
    cpu_model = platform.processor()

    # Windows version
    windows_version = platform.platform()

    # Uptime
    uptime_seconds = time.time() - psutil.boot_time()

    uptime_days = int(uptime_seconds // 86400)
    uptime_hours = int((uptime_seconds % 86400) // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)

    uptime = (
        f"{uptime_days}d "
        f"{uptime_hours}h "
        f"{uptime_minutes}m"
    )

    # IP address
    ip_address = socket.gethostbyname(
        socket.gethostname()
    )

    # Top memory-using programs
    processes = {}

    for process in psutil.process_iter(
        ["name", "memory_info"]
    ):
        try:

            name = process.info["name"]
            memory_used = process.info["memory_info"].rss

            if name in processes:
                processes[name] += memory_used
            else:
                processes[name] = memory_used

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            pass

    sorted_processes = sorted(
        processes.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_processes = []

    for name, memory_used in sorted_processes[:5]:

        top_processes.append({
            "name": name,
            "memory": round(
                memory_used / (1024 ** 2),
                2
            )
        })

    return {

        "computer_name": platform.node(),

        "windows_version": windows_version,

        "cpu_model": cpu_model,

        "physical_cores": physical_cores,

        "logical_processors": logical_processors,

        "cpu": cpu,

        "ram": memory.percent,

        "ram_total": round(
            memory.total / (1024 ** 3),
            2
        ),

        "ram_used": round(
            memory.used / (1024 ** 3),
            2
        ),

        "ram_available": round(
            memory.available / (1024 ** 3),
            2
        ),

        "disk": disk.percent,

        "disk_total": round(
            disk.total / (1024 ** 3),
            2
        ),

        "disk_used": round(
            disk.used / (1024 ** 3),
            2
        ),

        "disk_free": round(
            disk.free / (1024 ** 3),
            2
        ),

        "uptime": uptime,

        "ip_address": ip_address,

        "processes": top_processes
    }


if __name__ == "__main__":

    status = get_pc_status()

    response = requests.post(
        f"{RENDER_URL}/api/pc-status",
        json=status
    )

    print("Render response:", response.status_code)

    print(response.text)

    print()

    print("Windows PC Agent")
    print("----------------")

    for key, value in status.items():

        print(f"{key}: {value}")