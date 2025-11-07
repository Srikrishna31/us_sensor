import numpy as np
from typing import List, Dict, Any
from src.transformation import Transformation

from math import pi as PI

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
    def __init__(self, position_x, position_y, position_z, h, p, r, sensor_data: Dict[str, Any]):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.h = h
        self.p = p
        self.r = r
        self.transform = Transformation(np.array([position_x, position_y, position_z]), np.array([h, p, r]))
        self.sensors = []
        for name, sensor in sensor_data.items():
            self.sensors.append(UltrasonicSensor(id_=name, x=sensor["X_m"], y=sensor["Y_m"], z=sensor["Z_m"], h=sensor["yaw_rad"], p=sensor["pitch_rad"], r=sensor["roll_rad"],
                                             range_max=sensor["range_max_m"], range_min=sensor["range_min_m"], cone_angle_deg=sensor["fov_deg"]))


    def get_coordinates(self):
            return self.position_x, self.position_y, self.position_z, self.h, self.p, self.r

    def transform_from_outside_world_to_car_reference(self, obstacle: Obstacle):
        pts_world = np.vstack(obstacle.get_bounds())  # shape (8,3)
        car_pts = np.array([self.transform.apply_transformation(p)[0] for p in pts_world])
        return car_pts

    def get_sensors(self):
        return self.sensors

class UltrasonicSensor:
    def __init__(self, id_: str, x, y, z, h, p, r, range_min = 1, range_max = 4, cone_angle_deg = 0):

        self.range_min = range_min
        self.range_max = range_max
        self.position_x = x
        self.position_y = y
        self.position_z = z
        self.cone_angle_rad = cone_angle_deg * PI / 180
        
        self.h = h 
        self.p = p  
        self.r = r 

        self.ID = id_
        self.transform = Transformation(np.array([x, y, z]), np.array([h, p, r]))

    def detect_obstacle(self: "UltrasonicSensor", pts) -> bool:
        temp = [self._detect_obstacle_point(pt) for pt in pts]
        # print(f"Min distance point: {min(temp)}")
        # res = False
        # for p in temp:
        #     i
        res = False
        min_d = None
        for d, r in temp:
            if r:
                res = True
                if min_d is None:
                    min_d = d
                else:
                    min_d = min(d, min_d)



        return (res, min_d)

    # def detect_obstacle(self: "UltrasonicSensor", obj: "Obstacle") -> bool:
    #     print([self._detect_obstacle_point(pt) for pt in obj.get_bounds()])
    #     return any([self._detect_obstacle_point(pt) for pt in obj.get_bounds()])

    def _detect_obstacle_point(self:"UltrasonicSensor", point: np.ndarray) -> bool:
        v = point
        axis = np.array([1.0, 0.0, 0.0])
        dot_product = np.dot(axis, v)
        dist = np.linalg.norm(v)
        # print(dist)
        # if dist < self.range_min or dist > self.range_max:
        #     return False

        # print(dist)
        angle = np.arccos(dot_product / dist)
        is_negative = v / dist
        return (dist, angle <= self.cone_angle_rad and dist>= self.range_min and dist <= self.range_max and is_negative[0] > 0)

    def get_obstacle_point(self:"UltrasonicSensor", point: np.ndarray) -> bool:
        v = point
        axis = np.array([1.0, 0.0, 0.0])
        dot_product = np.dot(axis, v)
        dist = np.linalg.norm(v)
        # print(dist)
        # if dist < self.range_min or dist > self.range_max:
        #     return False

        # print(dist)
        angle = np.arccos(dot_product / dist)
        is_negative = v / dist
        return dist

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
