# PC Monitor

A Python Flask-based PC monitoring dashboard for Windows.

## Features

- CPU usage monitoring
- RAM usage monitoring
- Disk usage monitoring
- Top memory-using programs
- Computer information
- Windows version
- CPU information
- System uptime
- IP address
- Remote PC lock
- Remote PC shutdown
- Live monitoring updates

## Requirements

- Windows PC
- Python 3.13 or newer
- Flask
- psutil

## Installation

Clone the repository:

    git clone https://github.com/Alexatb/PC_Monitor.git

Go into the project folder:

    cd PC_Monitor

Install the required packages:

    python -m pip install -r requirements.txt

## Run the application

    python app.py

Open the dashboard in your browser:

    http://127.0.0.1:5000

To access it from another device on the same network, use the PC's IP address:

    http://YOUR-PC-IP:5000

## Important

The Lock and Shutdown features control the Windows PC running the application.

Do not expose this application directly to the public internet without adding authentication and other security protections.
