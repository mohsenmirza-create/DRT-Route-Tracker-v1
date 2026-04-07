import csv
import json

SHAPES_FILE = "shapes.txt"
BRANCH_MAP_FILE = "branch_map.json"
OUTPUT_FILE = "route_shapes.json"

# Load branch map (shape_id → branch_id)
with open(BRANCH_MAP_FILE, "r", encoding="utf-8") as f:
    branch_map = json.load(f)

# Load shapes grouped by shape_id
shapes = {}

with open(SHAPES_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        shape_id = row["shape_id"]
        lat = float(row["shape_pt_lat"])
        lon = float(row["shape_pt_lon"])
        seq = int(row["shape_pt_sequence"])

        if shape_id not in shapes:
            shapes[shape_id] = []

        shapes[shape_id].append((seq, lat, lon))

# Convert to branch-based shapes
branch_shapes = {}

for shape_id, pts in shapes.items():
    pts_sorted = sorted(pts, key=lambda x: x[0])
    coords = [[lat, lon] for (_, lat, lon) in pts_sorted]

    branch_id = branch_map.get(shape_id)
    if branch_id:
        branch_shapes[branch_id] = coords

# Save
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(branch_shapes, f, indent=2)

print("Saved route_shapes.json with", len(branch_shapes), "branch routes.")

