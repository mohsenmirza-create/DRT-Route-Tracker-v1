import json
import time
import webbrowser
import os

from http.server import SimpleHTTPRequestHandler, HTTPServer

from gtfs_loader import load_shape_coordinates
from bus_logic import Bus

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GTFS_DIR = os.path.join(BASE_DIR, "gtfs")

def write_position(lat, lon):
    with open("bus_position.json", "w") as f:
        json.dump({"lat": lat, "lon": lon}, f)

def start_server():
    server = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
    print("Server running at http://localhost:8000/map.html")
    server.serve_forever()

if __name__ == "__main__":
    coords = load_shape_coordinates(GTFS_DIR, route_id="900")
    bus = Bus(route_id="900", coordinates=coords)

    webbrowser.open("http://localhost:8000/map.html")

    import threading
    threading.Thread(target=start_server, daemon=True).start()

    while True:
        bus.move(dt=0.1)
        lat, lon = bus.get_position()
        write_position(lat, lon)
        time.sleep(0.1)
