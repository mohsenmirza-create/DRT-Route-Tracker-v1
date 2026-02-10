import folium
from bus_logic import ROUTE

# Center map on the first point
start_lat, start_lon = ROUTE[0]

m = folium.Map(location=[start_lat, start_lon], zoom_start=13)

# Draw the route
folium.PolyLine(ROUTE, color="blue", weight=4).add_to(m)

# Save the map
m.save("map.html")

print("Map generated as map.html")