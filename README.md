# DRT-Route-Tracker-v1
![CI](https://github.com/mohsenmirza-create/DRT-Route-Tracker-v1/actions/workflows/ci.yml/badge.svg)


Simulated Durham transit tracker using public data, covers all of Durham.
Our goal is to make a framework for being able to track any given drt bus on its route live.
We want to make this because all the other apps just show the route and there's not any way to see where any given bus is located.
We will be coding this in python.

HOW IT WORKS:
project is made up in 3 layers, 
-the DATA LAYER, where raw GTFS data is collected, and scripts are created that convert this into JSON lookups.
-The BACKEND, where GTFS is fetched in real time, it maps the vehicles to routes/branches, and it serves JSON APIs to the frontend
-The FRONTEND, where it displays routes, shows live bus positions, lets the user search for routes.


INSTRUCTIONS:
To clone the repo create a desktop folder, open terminal, then input "git clone-https://github.com/mohsenmirza-create/DRT-Route-Tracker-v1.git".
Navigate to the root folder, then click on run_server.bat.
That will open a terminal and your default web browser will open with the map now running.
To close the program, exit the web browser and close the opened terminal.
*ANOTHER OPTION
Download the zip file under releases titled "DRT v2.0.0".
Unzip and do the same as you would the cloned project.


INSTRUCTIONS FOR TESTING:
To test the project go into your root folder (DRT-Route-Tracker-v1), open a terminal and type "pytest -v". The test cases will appear and be verified.

INSTRUCTIONS FOR DOCKER:
-To run the project in Docker (you must first have Docker installed and running) input "docker build -t drt-route-tracker ." in a terminal within the project root.
-Run the container by inputting "docker run -p 8080:8000 drt-route-tracker" within the same terminal.
-Open the application by inputting "http://localhost:8080/map.html" in a web browser.

PROJECT Structure: 
3 main python folders: main, gtfs, and tests.

PROJECT Limtations:
Bus updates are slow (roughly every 40 seconds).
Limited sidebar (needs improvement on features).


Project Performance Improvements:
-Removed Route ID, Bearing, and Speed. (Currently unused)
-Dramatically increased performance (JSON file size down to roughly 7k bytes, formerly 25k bytes, download time reduced from 2 - 3 ms, to 0.8 ms).

What I've Learned:
-I had to learn what GTFS data is (how transit agencies structure their data, How to map trips, and how to preprocess GTFS into a usable JSON).
-I had to learn how to create a backend that ouotputs real-time data (how to fetch the GTFS feed that DRT provides, turn them into python objects, and assign them vehicle ID's).
-Creating a UI (getting familiar with HTML, making a sidebar with routes and branches, search filtering and auto complete, highlighting routes on the map, and making it readable by dimming non selected buses).
-Working with mapping libraries, specifically leaflet (How to draw polylines for routes, how to place markers for buses, and how to update markers).
-Major issues I had was personal management, I'd accidently delete git clones that I hadn't properly saved and had to back track a lot, my project folders on my laptop were disorganized. Learning how to use HTML was it's own process. I wasted a lot of time starting from using simulated data instead of jumping straight to real data since I created a whole system where the bus project would create intricate coordinates points based off of the static data given in the gtfs folder.

FUTURE PLANS:
-Update the UI (improve readability, add borders between bus options, create a proper drop down menu with arrows, change font, make it look nicer in general).
-Include extra information (highlight bus stops, show ETA's, display the bus's current speed, show arrows on the highlighted route to show which direction the selected bus is going in.).










