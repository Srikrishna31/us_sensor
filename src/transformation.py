import numpy as np
from scipy.spatial.transform import Rotation as R

class Transformation:
    # def __init__(self, coordinates, angles):
    #     self.coordinates = coordinates
    #     self.angles = angles
    #     self.T, self.T_inv = Transformation.create_transformation_matrix(coordinates, angles)

    # @staticmethod
    # def create_transformation_matrix(coordinates, angles):
    #     rotation = R.from_euler('zyx', angles, degrees=False)
    #     rot_matrix = rotation.as_matrix()
    #     T = np.eye(4)
    #     T[:3, :3] = rot_matrix
    #     T[:3, 3] = coordinates
    #     T_inv = np.linalg.inv(T)
    #     return T, T_inv

    @staticmethod
    def euler_to_rotation_matrix(yaw, pitch, roll):
        Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])
        Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
        Rx = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])

        return np.dot(Rz, np.dot(Ry, Rx))

    def __init__(self, vehicle_position, vehicle_orientation):
        self.vehicle_position = vehicle_position
        self.vehicle_orientation = vehicle_orientation
        # self.T, self.T_inv = Transformation.create_transformation_matrix(coordinates, angles)
        # def apply_transformation(point_world, vehicle_position, vehicle_orientation):``
        # Unpack vehicle position and orientation
        x_vehicle, y_vehicle, z_vehicle = vehicle_position
        yaw_vehicle, pitch_vehicle, roll_vehicle = vehicle_orientation
    
        # Calculate rotation matrix
        self.R_vehicle_world = Transformation.euler_to_rotation_matrix(yaw_vehicle, pitch_vehicle, roll_vehicle)
    
        # Calculate inverse rotation matrix
        self.R_vehicle_world_inv = np.linalg.inv(self.R_vehicle_world)


    def apply_transformation(self, point_cordinates, point_orientation=None):
        # np.append(coords, 1)
        # transformed_points = self.T_inv @ object_coords
        # return transformed_points, angles
        # Transform point to vehicle coordinate
        point_vehicle = np.dot(self.R_vehicle_world_inv, (point_cordinates - self.vehicle_position))
    
        return point_vehicle , point_orientation