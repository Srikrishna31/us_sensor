from __future__ import annotations
import numpy as np

def calculate_3d_distance(ego, obstacle):
    dx = ego.position_x - obstacle.position_x
    dy = ego.position_y - obstacle.position_y
    dz = ego.position_z - obstacle.position_z
    return (dx**2 + dy**2 + dz**2) ** 0.5
class Obstacle:
    # the obstacle coordinate will be given by an outside file and it is related to an extern reference system
    def __init__(self, position_x, position_y, position_z, width, height, depth, ID: str ="1"):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.width = width
        self.height = height
        self.depth = depth
        self.ID = ID

    def get_bounds(self):
        return (self.position_x, self.position_y, self.position_z, self.width, self.height, self.depth)


class EGO:
    def __init__(self, position_x, position_y, position_z, h, p, r):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        # heading / yaw, pitch, roll in degrees
        self.h = h
        self.p = p
        self.r = r
        

    def transform_from_outside_world_to_car_reference(self, obstacle: Obstacle):
       # needs implementation
       return 1
    

    
    def get_coordinates(self):
        return (self.position_x, self.position_y, self.position_z, self.h, self.p, self.r)
    

class UltrasonicSensor:
    def __init__(self, x, y, z, h, p, r, ID: str,  range_min_m = 1, range_max_m = 5):

        self.range_min_m = range_min_m
        self.max_range_m = range_max_m
        self.position_x = x
        self.position_y = y
        self.position_z = z
        
        # sensor orientation (relative to car) in degrees
        self.h = h
        self.p = p
        self.r = r

        self.ID = ID

    def detect_obstacle(self, distance_m):
        # returns True if within sensor min/max range (meters)
        return (self.range_min_m <= distance_m <= self.max_range_m)


    def transform_from_car_to_sensor_reference(self, point_in_car_coords):
       return 2
