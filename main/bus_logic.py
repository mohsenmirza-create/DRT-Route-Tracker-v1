import math

class Bus:
    def __init__(self, route_id, coordinates, speed_mps=8):
        self.route_id = route_id
        self.coordinates = coordinates
        self.speed_mps = speed_mps
        self.index = 0
        self.progress = 0.0

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

    def move(self, dt):
        if self.index >= len(self.coordinates) - 1:
            self.index = 0
            self.progress = 0.0

        lat1, lon1 = self.coordinates[self.index]
        lat2, lon2 = self.coordinates[self.index + 1]

        segment_length = self.haversine(lat1, lon1, lat2, lon2)
        distance_to_move = self.speed_mps * dt
        progress_step = distance_to_move / segment_length

        self.progress += progress_step

        if self.progress >= 1.0:
            self.index = (self.index + 1) % len(self.coordinates)
            self.progress = 0.0

    def get_position(self):
        lat1, lon1 = self.coordinates[self.index]
        lat2, lon2 = self.coordinates[(self.index + 1) % len(self.coordinates)]
        lat = lat1 + (lat2 - lat1) * self.progress
        lon = lon1 + (lon2 - lon1) * self.progress
        return lat, lon
