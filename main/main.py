import tkinter as tk
import folium
import tempfile
import webbrowser
from bus_logic import Bus

bus = Bus()

def open_map_in_browser():
    # Move bus before generating map
    bus.move()
    lat, lon = bus.get_position()

    #bus position
    m = folium.Map(location=[lat, lon], zoom_start=15)

    #set marker for bus
    folium.Marker(
        [lat, lon],
        popup="Bus 401",
        icon=folium.Icon(color="red", icon="bus", prefix="fa")
    ).add_to(m) 
    
    # Save to a temporary HTML file and open it in the default browser
    tmp = tempfile.NamedTemporaryFile(prefix="drt_map_", suffix=".html", delete=False)
    m.save(tmp.name)
    webbrowser.open("file://" + tmp.name)

root = tk.Tk()
root.title("DRT Route Tracker")
root.geometry("480x320")

# Placeholder menu
blank_frame = tk.Frame(root, bg="white")
blank_frame.pack(fill=tk.BOTH, expand=True)

# Button to open the map
open_map_btn = tk.Button(root, text="Open Map", command=open_map_in_browser, width=16)
open_map_btn.pack(pady=12)

root.mainloop()


