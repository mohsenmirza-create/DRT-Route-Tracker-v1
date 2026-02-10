ROUTE = [
    (43.9448472, -78.8917028),
    (43.9425, -78.8900),
    (43.9400, -78.8890),
    (43.9375, -78.8880),
    (43.9350, -78.8870),
]

class Bus:
    def __init__(self):
        self.route = ROUTE
        self.index = 0
        self.progress = 0.0  # 0 → 1 between points

    def get_position(self):
        lat1, lon1 = self.route[self.index]
        lat2, lon2 = self.route[(self.index + 1) % len(self.route)]

        # linear interpolation
        lat = lat1 + (lat2 - lat1) * self.progress
        lon = lon1 + (lon2 - lon1) * self.progress
        return lat, lon

    def move(self, step=0.05):
        self.progress += step
        if self.progress >= 1.0:
            self.progress = 0.0
            self.index = (self.index + 1) % len(self.route)