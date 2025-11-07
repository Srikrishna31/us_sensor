from __future__ import annotations
import numpy as np
from typing import List

def calculate_3d_distance(ego, obstacle):
    dx = ego.position_x - obstacle.position_x
    dy = ego.position_y - obstacle.position_y
    dz = ego.position_z - obstacle.position_z
    return (dx**2 + dy**2 + dz**2) ** 0.5

class UltrasonicSensor:
    def __init__(self, id_: str, x, y, z, h, p, r, range_min = 1, range_max = 4, cone_angle = 0):

        self.range_min = range_min
        self.range_max = range_max
        self.position_x = x
        self.position_y = y
        self.position_z = z
        self.cone_angle = cone_angle

        self.h = h
        self.p = p
        self.r = r

        self.ID = id_

    def detect_obstacle(self:"UltrasonicSensor", point: np.ndarray) -> bool:
        v = point
        axis = np.array([1.0, 1.0, 1.0])
        dot_product = np.dot(axis, v)
        angle = np.arccos(dot_product / np.linalg.norm(v))
        dist = np.linalg.norm(v)
        return angle <= self.cone_angle and self.range_min >= dist and dist <= self.range_max

    def ego_to_sensor(self, ego_coordinates):
        sensor_x = ego_coordinates[0] - self.position_x
        sensor_y = ego_coordinates[1] - self.position_y
        sensor_z = ego_coordinates[2] - self.position_z
        return (sensor_x**2 + sensor_y**2 + sensor_z**2) ** 0.5


class EGO:
    def __init__(self, position_x, position_y, position_z, h, p, r):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.h = h
        self.p = p
        self.r = r

    def get_coordinates(self):
        return self.position_x, self.position_y, self.position_z, self.h, self.p, self.r


class Obstacle:
    # the obstacle coordinate will be given by an outside file and it is related to an extern reference system
    def __init__(self, position_x, position_y, position_z, width, height, depth, id:str):
        half_width = width / 2
        half_height = height / 2
        half_depth = depth / 2
        self.front_left_bottom = np.array([position_x - half_width, position_y - half_height, position_z + half_depth])
        self.front_right_bottom = np.array([position_x + half_width, position_y - half_height, position_z + half_depth])
        self.back_left_bottom = np.array([position_x - half_width, position_y - half_height, position_z - half_depth])
        self.back_right_bottom = np.array([position_x + half_width, position_y - half_height, position_z - half_depth])
        self.front_left_top = np.array([position_x - half_width, position_y + half_height, position_z + half_depth])
        self.front_right_top = np.array([position_x + half_width, position_y + half_height, position_z + half_depth])
        self.back_left_top = np.array([position_x - half_width, position_y + half_height, position_z - half_depth])
        self.back_right_top = np.array([position_x + half_width, position_y + half_height, position_z - half_depth])
        self.id = id

    def get_bounds(self) -> List[np.ndarray]:
        return [self.front_left_top, self.front_right_top, self.back_left_top, self.back_right_top,
                self.front_left_bottom, self.front_right_bottom, self.back_left_bottom, self.back_right_bottom]

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
