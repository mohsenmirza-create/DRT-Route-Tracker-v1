import json
import webbrowser
import os
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer

print(">>> SERVER IS SERVING FROM:", os.getcwd())

# ---------- GTFS STATIC FILES ----------
with open("gtfs/trip_to_shape.json", "r") as f:
    trip_to_shape = json.load(f)

with open("gtfs/branch_map.json", "r") as f:
    branch_map = json.load(f)

# ---------- GTFS-RT SETUP ----------
import requests
from google.transit import gtfs_realtime_pb2

GTFS_RT_URL = "https://drtonline.durhamregiontransit.com/gtfsrealtime/VehiclePositions"

# ---------- CACHE SETTINGS ----------
CACHE_TTL = 10.0  # seconds
_last_fetch_time = 0
_last_vehicle_data = None


def load_gtfs_from_url():
    """Load GTFS-RT vehicle positions from a live URL."""
    feed = gtfs_realtime_pb2.FeedMessage()
    resp = requests.get(GTFS_RT_URL, timeout=10)
    resp.raise_for_status()
    feed.ParseFromString(resp.content)
    return feed


def get_realtime_vehicles():
    """
    Returns a list of:
    {id, lat, lon, route_id, branch}
    Uses caching to reduce repeated GTFS-RT downloads.
    """

    global _last_fetch_time, _last_vehicle_data

    start_time = time.time()

    # ---------- CACHE HIT ----------
    if _last_vehicle_data is not None and (time.time() - _last_fetch_time) < CACHE_TTL:
        duration_ms = (time.time() - start_time) * 1000
        print(f"[CACHE] Served vehicles in {duration_ms:.2f} ms")
        return _last_vehicle_data

    # ---------- CACHE MISS ----------
    feed = load_gtfs_from_url()

    vehicles = []

    for entity in feed.entity:
        if not entity.HasField("vehicle"):
            continue

        v = entity.vehicle
        if not v.HasField("position"):
            continue

        # Safely extract shape_id (GTFS-RT often omits it)
        shape_id = getattr(v.trip, "shape_id", None)

        # If missing, infer from trip_id
        if not shape_id and v.trip.trip_id in trip_to_shape:
            shape_id = trip_to_shape[v.trip.trip_id]

        # Look up branch if shape_id exists
        branch = branch_map.get(shape_id)

        vehicles.append({
            "id": v.vehicle.id or entity.id,
            "lat": v.position.latitude,
            "lon": v.position.longitude,
            "route_id": v.trip.route_id if v.HasField("trip") else None,
            "branch": branch
        })

    # Update cache
    _last_vehicle_data = vehicles
    _last_fetch_time = time.time()

    duration_ms = (_last_fetch_time - start_time) * 1000
    print(f"[FETCH] Download + parse took {duration_ms:.2f} ms")

    return vehicles


# ---------- BUILD /branches ----------
def load_branches():
    """
    Builds authoritative branch definitions using:
    - trip_to_shape.json (trip → shape)
    - branch_map.json (shape → branch)
    - trips.txt (route_id + raw trip_headsign)
    
    Returns:
    [
      {"route_id": "216", "branch_id": "216A", "description": "Audley / Ajax Station"},
      ...
    ]
    """

    trips_path = "gtfs/trips.txt"
    if not os.path.exists(trips_path):
        print("ERROR: gtfs/trips.txt not found!")
        return []

    # branch_id → {route_id, descriptions[]}
    branch_info = {}

    with open(trips_path, "r", encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        idx_route = header.index("route_id")
        idx_headsign = header.index("trip_headsign")
        idx_trip = header.index("trip_id")

        for line in f:
            parts = line.strip().split(",")
            if len(parts) <= idx_trip:
                continue

            trip_id = parts[idx_trip]
            route_id = parts[idx_route]
            headsign = parts[idx_headsign]

            # trip → shape
            shape_id = trip_to_shape.get(trip_id)
            if not shape_id:
                continue

            # shape → branch
            branch_id = branch_map.get(shape_id)
            if not branch_id:
                continue

            if branch_id not in branch_info:
                branch_info[branch_id] = {
                    "route_id": route_id,
                    "descriptions": set()
                }

            branch_info[branch_id]["descriptions"].add(headsign)

    # Convert to final list
    result = []
    for branch_id, info in branch_info.items():
        desc = " / ".join(sorted(info["descriptions"]))
        result.append({
            "route_id": info["route_id"],
            "branch_id": branch_id,
            "description": desc
        })

    print(f"[BRANCHES] Built {len(result)} branches")
    return result


# ---------- HTTP HANDLER ----------
class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/vehicles"):
            self.handle_vehicles()
            return

        if self.path.startswith("/branches"):
            self.handle_branches()
            return

        return super().do_GET()

    # ---------- /vehicles ----------
    def handle_vehicles(self):
        try:
            t0 = time.time()
            vehicles = get_realtime_vehicles()
            t1 = time.time()

            json_start = time.time()
            body = json.dumps({"vehicles": vehicles}).encode("utf-8")
            json_end = time.time()

            vehicle_fetch_ms = (t1 - t0) * 1000
            json_build_ms = (json_end - json_start) * 1000
            json_size_bytes = len(body)

            print(f"[MEASURE] Vehicle processing time: {vehicle_fetch_ms:.2f} ms")
            print(f"[MEASURE] JSON build time: {json_build_ms:.2f} ms")
            print(f"[MEASURE] JSON size: {json_size_bytes} bytes")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except Exception as e:
            err = {"error": str(e)}
            body = json.dumps(err).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    # ---------- /branches ----------
    def handle_branches(self):
        try:
            branches = load_branches()
            body = json.dumps(branches).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except Exception as e:
            err = {"error": str(e)}
            body = json.dumps(err).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


# ---------- START SERVER ----------
def start_server():
    server = HTTPServer(("0.0.0.0", 8000), MyHandler)
    print("Server running at http://localhost:8000/map.html")
    server.serve_forever()


if __name__ == "__main__":
    webbrowser.open("http://localhost:8000/map.html")
    start_server()
