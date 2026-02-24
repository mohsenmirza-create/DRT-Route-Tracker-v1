import json
import webbrowser
import os
import subprocess
import time
from bus_logic import Bus

bus = Bus()

def write_position(lat, lon):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "bus_position.json")

    with open(json_path, "w") as f:
        json.dump({"lat": lat, "lon": lon}, f)

def update_bus():
    while True:
        bus.move(dt=0.1)
        lat, lon = bus.get_position()
        write_position(lat, lon)
        time.sleep(0.1)  # 10 updates per second

def start_server():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen(
        ["python", "-m", "http.server", "8000"],
        cwd=script_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)  # give server time to start

def open_map():
    webbrowser.open("http://localhost:8000/map.html")

if __name__ == "__main__":
    start_server()
    open_map()
    update_bus()

