import numpy as np
from scipy.spatial.transform import Rotation as R

def create_transformation_matrix(coordinates, angles):
    rotation = R.from_euler('zyx', angles, degrees=False)
    rot_matrix = rotation.as_matrix()

    T = np.eye(4)
    T[:3, :3] = rot_matrix
    T[:3, 3] = coordinates
    return T

