#Ontario Tech to Simcoe
ROUTE = [
    (43.9448472, -78.8917028),   # Ontario Tech
    (43.9425, -78.8900),
    (43.9400, -78.8890),
    (43.9375, -78.8880),
    (43.9350, -78.8870),
]

class Bus:
    def __init__(self):
        self.index = 0

    def get_position(self):
        return ROUTE[self.index]

    def move(self):
        # Move to next point then loop at end
        self.index = (self.index + 1) % len(ROUTE)