class UltrasonicSensor:
    def __init__(self, range_min_cm = 100, range_max_cm = 400):
        # range minimum distance to detect an obstacle
        self.range_min_cm = range_min_cm
        # range to maximum distance to detect an obstacle
        self.max_range_cm = range_max_cm

    def detect_obstacle(self, distance_cm):
       # should be updated later
        if self.range_min_cm <= distance_cm <= self.max_range_cm:
            return True
        else:
            return False

def calculate_3d_distance(ego, obstacle):
    # will be updated later
    dx = ego.position_x - obstacle.position_x
    dy = ego.position_y - obstacle.position_y
    dz = ego.position_z - obstacle.position_z
    return (dx**2 + dy**2 + dz**2) ** 0.5

class Obstacle:
    def __init__(self, position_x, position_y, position_z, width, height, depth):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.width = width
        self.height = height
        self.depth = depth

class EGO:
    def __init__(self, position_x, position_y, position_z):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z

    def get_coordinates(self):
        return (self.position_x, self.position_y, self.position_z)

if __name__=="__main__":
    print("Hello World")
