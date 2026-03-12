# DRT-Route-Tracker-v1
![CI](https://github.com/mohsenmirza-create/DRT-Route-Tracker-v1/actions/workflows/ci.yml/badge.svg)

Simulated Durham transit tracker using public data, covers all of Durham.
Our goal is to make a framework for being able to track any given drt bus on its route live.
We want to make this because all the other apps just show the route and there's not any way to see where any given bus is located.
We will be coding this in python.
Our goals include having a map fuction to calculate the most efficient route to a destination.
This will be a framework tracking busses hypothetically in a limited area. 
Any busses that leave the area will no longer be shown but still tracked in the background.


INSTRUCTIONS:
To clone the repo create a desktop folder, open terminal, then input "git clone-https://github.com/mohsenmirza-create/DRT-Route-Tracker-v1.git".
Navigate to the main folder then run main.py (bus_logic is imported into main).
Click Open Map.
Bus route updates each time map is opened. (Bus will not update unless page is closed and reopened, reloads do not work.)
Bus will travel to set coordinates and loop when route is complete.
*ANOTHER OPTION
Download the zip file under releases titled "DRT-Route-Tracker-v1.1.0".
Unzip and run "main.py" within the "main" folder


INSTRUCTIONS FOR TESTING:
To test the project go into your root folder (DRT-Route-Tracker-v1), open a terminal and type "pytest -v". The test cases will appear and be verified.

PROJECT Structure: 
3 main python folders MAIN, DRT-UI, DRT-Data
Main is the actual function of the code. 
DRT-UI contaions the frontend that the user will see including the map and the the busses. 
DRT-Data will contain the Bus and route data becuase this is a simulated map none of the bus data is real so we have to simulate it.


PROJECT Limtations:
Only one Bus.
Map does not auto update.
No animations 
Bus markers need updates.







