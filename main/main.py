import tkinter as tk
import folium
import tempfile
import webbrowser

#Start Coordinates (Ontario Tech)
Lat = 43.94571375306523
Lon = -78.89763878336528

def open_map_in_browser():
    # Create a folium map
    map = folium.Map(location=[Lat, Lon], zoom_start=18)
    

    # Save to a temporary HTML file and open it in the default browser
    tmp = tempfile.NamedTemporaryFile(prefix="drt_map_", suffix=".html", delete=False)
    map.save(tmp.name)
    webbrowser.open("file://" + tmp.name)

root = tk.Tk()
root.title("DRT Route Tracker")
root.geometry("480x320")

# Placeholder menu
blank_frame = tk.Frame(root, bg="white")

# Button to open the map
open_map_btn = tk.Button(root, text="Open Map", command=open_map_in_browser, width=16)
open_map_btn.pack(pady=10)

root.mainloop()