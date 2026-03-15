import math

# We no longer import ROUTE because GTFS removed the hardcoded route.
# Instead, we define a tiny test route that behaves the same way.
from main.bus_logic import Bus

# A tiny route so the bus can cross segment boundaries during tests
TEST_ROUTE = [
    (43.0, -79.0),
    (43.00001, -79.00001),
    (43.00002, -79.00002)
]

def test_route_not_empty():
    assert len(TEST_ROUTE) > 2  # checks if the route has more than 2 coordinate points so the bus has a valid path to follow

def test_interpolation_midpoint(): 
    bus = Bus(route_id="test", coordinates=TEST_ROUTE)  # creates a new bus instance using the test route and default speed
    # forces the bus to pass between 0 and 1
    bus.index = 0 
    bus.progress = 0.5
    # takes coordinates of first two route points and calculates the midpoint
    lat1, lon1 = TEST_ROUTE[0] 
    lat2, lon2 = TEST_ROUTE[1]

    lat, lon = bus.get_position()  # asks the bus its current position based off of index and progress

    # checks that the bus latitude and longitude are at the midpoint
    assert math.isclose(lat, (lat1 + lat2) / 2, rel_tol=1e-5)
    assert math.isclose(lon, (lon1 + lon2) / 2, rel_tol=1e-5)

def test_progress_resets_and_advances_index():
    bus = Bus(route_id="test", coordinates=TEST_ROUTE)  # new bus instance
    # places bus just before next point
    bus.index = 0
    bus.progress = 0.999  # forces it near the boundary

    bus.move(dt=0.1)  # moves forward

    assert 0.0 <= bus.progress < 1.0  # checks that progress has been reset into a valid range for the next segment
    assert bus.index == 1  # checks that the bus advanced to the next segment index

def test_constant_speed_behavior():
    bus = Bus(route_id="test", coordinates=TEST_ROUTE, speed_mps=10)

    lat_before, lon_before = bus.get_position()
    bus.move(dt=0.1)
    lat_after, lon_after = bus.get_position()

    # Distance moved should be close to speed * dt
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

    dist = haversine(lat_before, lon_before, lat_after, lon_after)

    assert math.isclose(dist, 10 * 0.1, rel_tol=0.3)
