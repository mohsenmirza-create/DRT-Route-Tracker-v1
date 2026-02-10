import requests
import json

# Your start/end
start_lat, start_lon = 43.94479484949457, -78.85086903668632
end_lat, end_lon   = 43.94667030177077, -78.89407612530077

def get_osrm_route(start_lat, start_lon, end_lat, end_lon):
    base_url = "http://router.project-osrm.org/route/v1/driving"
    # OSRM expects lon,lat
    coords = f"{start_lon},{start_lat};{end_lon},{end_lat}"
    params = {
        "overview": "full",
        "geometries": "geojson"
    }
    url = f"{base_url}/{coords}"
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()

    # GeoJSON: [ [lon, lat], ... ]
    coords = data["routes"][0]["geometry"]["coordinates"]

    # Flip to (lat, lon) tuples for your code
    route = [(lat, lon) for lon, lat in coords]
    return route

if __name__ == "__main__":
    route = get_osrm_route(start_lat, start_lon, end_lat, end_lon)

    # Print as a Python list you can paste into bus_logic.py
    print("ROUTE = [")
    for lat, lon in route:
        print(f"    ({lat:.8f}, {lon:.8f}),")
    print("]")