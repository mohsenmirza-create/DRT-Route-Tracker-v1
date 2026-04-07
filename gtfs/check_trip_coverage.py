import json

# Load trip_to_shape.json (same folder)
with open("trip_to_shape.json") as f:
    trip_to_shape = json.load(f)

# Load trips.txt (same folder)
with open("trips.txt") as f:
    header = f.readline().strip().split(",")
    idx_trip = header.index("trip_id")

    missing = []
    total = 0

    for line in f:
        parts = line.strip().split(",")
        if len(parts) <= idx_trip:
            continue

        trip_id = parts[idx_trip]
        total += 1

        if trip_id not in trip_to_shape:
            missing.append(trip_id)

print(f"Total trips: {total}")
print(f"Trips missing from trip_to_shape.json: {len(missing)}")

if missing:
    print("Example missing trip_ids:")
    print(missing[:20])
else:
    print("All trips are covered!")

