import csv

def load_shape_coordinates(gtfs_folder, route_id):
    shapes_path = f"{gtfs_folder}/shapes.txt"
    trips_path = f"{gtfs_folder}/trips.txt"

    # Step 1: find shape_id for the given route
    shape_id = None
    with open(trips_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["route_id"] == route_id:
                shape_id = row["shape_id"]
                break

    if shape_id is None:
        raise ValueError(f"No shape found for route_id {route_id}")

    # Step 2: load coordinates for that shape
    coords = []
    with open(shapes_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["shape_id"] == shape_id:
                lat = float(row["shape_pt_lat"])
                lon = float(row["shape_pt_lon"])
                seq = int(row["shape_pt_sequence"])
                coords.append((seq, lat, lon))

    coords.sort(key=lambda x: x[0])
    return [(lat, lon) for (_, lat, lon) in coords]
