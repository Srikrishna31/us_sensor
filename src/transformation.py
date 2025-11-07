import numpy as np
from scipy.spatial.transform import Rotation as R

class Transformation:
    def __init__(self, coordinates, angles):
        self.coordinates = coordinates
        self.angles = angles
        self.T, self.T_inv = Transformation.create_transformation_matrix(coordinates, angles)

    @staticmethod
    def create_transformation_matrix(coordinates, angles):
        rotation = R.from_euler('zyx', angles, degrees=False)
        rot_matrix = rotation.as_matrix()
        T = np.eye(4)
        T[:3, :3] = rot_matrix
        T[:3, 3] = coordinates
        T_inv = np.linalg.inv(T)
        return T, T_inv

    def apply_transformation(self, object_coords):
        transformed_points = self.T_inv @ object_coords
        return transformed_points
