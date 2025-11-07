import numpy as np
from typing import List
from src.transformation import Transformation

def calculate_3d_distance(ego, obstacle):
    dx = ego.position_x - obstacle.position_x
    dy = ego.position_y - obstacle.position_y
    dz = ego.position_z - obstacle.position_z
    return (dx**2 + dy**2 + dz**2) ** 0.5

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


class EGO:
    def __init__(self, position_x, position_y, position_z, h, p, r):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.h = h
        self.p = p
        self.r = r
        self.transform = Transformation(np.array([position_x, position_y, position_z]), np.array([h, p, r]))

    def get_coordinates(self):
        return self.position_x, self.position_y, self.position_z, self.h, self.p, self.r

    def transform_from_outside_world_to_car_reference(self, obstacle: Obstacle):
        pts_world = np.vstack(obstacle.get_bounds())  # shape (8,3)
        car_pts = np.array([self.transform.apply_transformation(p)[0] for p in pts_world])
        return car_pts


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
        self.transform = Transformation(np.array([x, y, z]), np.array([h, p, r]))

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

    def transform_from_car_to_sensor_reference(self, car_coords_obj):
        if isinstance(car_coords_obj, tuple):
            car_coords_obj = car_coords_obj[0]
        pts = np.asarray(car_coords_obj, dtype=float)
        if pts.ndim == 1:
            return self.transform.apply_transformation(pts)[0]
        elif pts.ndim == 2:
            return np.array([self.transform.apply_transformation(p)[0] for p in pts])
        else:
            raise ValueError("car_coords_obj must be shape (3,) or (N,3)")
