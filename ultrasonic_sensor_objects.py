def calculate_3d_distance(ego, obstacle):
    dx = ego.position_x - obstacle.position_x
    dy = ego.position_y - obstacle.position_y
    dz = ego.position_z - obstacle.position_z
    return (dx**2 + dy**2 + dz**2) ** 0.5

class UltrasonicSensor:
    def __init__(self, range_min_cm = 100, range_max_cm = 400, h, p, r):

        self.range_min_cm = range_min_cm
        self.max_range_cm = range_max_cm
        
        self.h = h 
        self.p = p  
        self.r = r 

    def detect_obstacle(self, distance_cm):
        if self.range_min_cm <= distance_cm <= self.max_range_cm:
            return True
        else:
            return False
    
    def ego_to_sensor(self, ego_coordinates):
        sensor_x = ego_coordinates[0] - self.position_x
        sensor_y = ego_coordinates[1] - self.position_y
        sensor_z = ego_coordinates[2] - self.position_z
        return (sensor_x**2 + sensor_y**2 + sensor_z**2) ** 0.5

class Obstacle:
    # the obstacle coordinate will be given by an outside file and it is related to an extern reference system
    def __init__(self, position_x, position_y, position_z, width, height, depth):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.width = width
        self.height = height
        self.depth = depth

    def get_bounds(self):
        return (self.position_x, self.position_y, self.position_z, self.width, self.height, self.depth)
    
    def transform_to_car_from_obstacle(self, ego: EGO):
        return (
            ego.position_x - self.position_x,
            ego.position_y - self.position_y,
            ego.position_z - self.position_z
        )

class EGO:
    def __init__(self, position_x, position_y, position_z, h, p, r):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.h = h
        self.p = p
        self.r = r

    def get_coordinates(self):
        return (self.position_x, self.position_y, self.position_z, self.h, self.p, self.r)
    
