import csv
import json
from collections import defaultdict

TRIPS_FILE = "trips.txt"
OUTPUT_FILE = "branch_map.json"

route_to_shapes = defaultdict(set)

# Load all shape_ids grouped by route_id
with open(TRIPS_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        route_id = row["route_id"]
        shape_id = row["shape_id"]
        route_to_shapes[route_id].add(shape_id)

branch_map = {}

# Assign branch letters A, B, C...
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for route_id, shapes in route_to_shapes.items():
    shapes = sorted(list(shapes))
    for i, shape_id in enumerate(shapes):
        branch_map[shape_id] = f"{route_id}{letters[i]}"

# Save as REAL JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(branch_map, f, indent=2)

print("Saved branch_map.json with", len(branch_map), "entries.")

