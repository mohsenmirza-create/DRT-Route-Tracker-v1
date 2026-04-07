import csv
import json

TRIPS_FILE = "trips.txt"
OUTPUT_FILE = "trip_to_shape.json"

trip_to_shape = {}

with open(TRIPS_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        trip_id = row["trip_id"]
        shape_id = row["shape_id"]
        trip_to_shape[trip_id] = shape_id

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(trip_to_shape, f, indent=2)

print("Saved trip_to_shape.json with", len(trip_to_shape), "entries.")
