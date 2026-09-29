from flask import Flask, jsonify, render_template, request
import os
import platform
import socket
import time
import psutil
import ctypes

app = Flask(__name__)

latest_pc_status = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status")
def status():

    # CPU
    cpu = psutil.cpu_percent(interval=1)

    # RAM
    memory = psutil.virtual_memory()

    # Disk
    disk = psutil.disk_usage("/")

    # Processes
    processes = {}

    for process in psutil.process_iter(["name", "memory_info"]):
        try:
            name = process.info["name"]
            memory_used = process.info["memory_info"].rss

            if name in processes:
                processes[name] += memory_used
            else:
                processes[name] = memory_used

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort processes by memory usage
    sorted_processes = sorted(
        processes.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Get top 5 processes
    top_processes = []

    for name, memory_used in sorted_processes[:5]:
        top_processes.append({
            "name": name,
            "memory": round(memory_used / (1024 ** 2), 2)
        })

    # PC information
    computer_name = platform.node()
    windows_version = platform.platform()
    cpu_model = platform.processor()
    physical_cores = psutil.cpu_count(logical=False)
    logical_processors = psutil.cpu_count(logical=True)

    # System uptime
    uptime_seconds = time.time() - psutil.boot_time()

    uptime_days = int(uptime_seconds // 86400)
    uptime_hours = int((uptime_seconds % 86400) // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)

    uptime = (
        f"{uptime_days}d "
        f"{uptime_hours}h "
        f"{uptime_minutes}m"
    )

    # PC IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Return local server information
    return jsonify({
        "cpu": cpu,

        "ram": memory.percent,
        "ram_total": round(memory.total / (1024 ** 3), 2),
        "ram_used": round(memory.used / (1024 ** 3), 2),
        "ram_available": round(memory.available / (1024 ** 3), 2),

        "disk": disk.percent,
        "disk_total": round(disk.total / (1024 ** 3), 2),
        "disk_used": round(disk.used / (1024 ** 3), 2),
        "disk_free": round(disk.free / (1024 ** 3), 2),

        "processes": top_processes,

        "computer_name": computer_name,
        "windows_version": windows_version,
        "cpu_model": cpu_model,
        "physical_cores": physical_cores,
        "logical_processors": logical_processors,
        "uptime": uptime,
        "ip_address": ip_address
    })


# Receive PC information from PC Agent
@app.route("/api/pc-status", methods=["POST"])
def receive_pc_status():

    global latest_pc_status

    data = request.get_json()

    latest_pc_status = data

    print("PC Agent data received:")
    print(latest_pc_status)

    return jsonify({
        "message": "PC status received successfully"
    })


# Return the latest information from the user's PC
@app.route("/api/command")
def get_command():
    return jsonify({"command": "none"})


# Lock the PC
@app.route("/lock", methods=["POST"])
def lock():
    ctypes.windll.user32.LockWorkStation()
    return jsonify({"message": "PC is locked"})


# Shutdown the PC
@app.route("/shutdown", methods=["POST"])
def shutdown():
    os.system("shutdown /s /t 0")
    return jsonify({"message": "PC is shutting down"})


# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)