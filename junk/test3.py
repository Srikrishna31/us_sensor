import numpy as np
# from scipy.spatial.transform import Rotation as R
from transformation import Transformation

# def create_transformation_matrix(coordinates, angles):
#     rotation = R.from_euler('zyx', angles, degrees=False)
#     rot_matrix = rotation.as_matrix()

#     T = np.eye(4)
#     T[:3, :3] = rot_matrix
#     T[:3, 3] = coordinates
#     return T
transformer = Transformation([1.828963, -138.407091, -0.006], [1.571584, -0.004266, -0.000046])
# ego_translation = [1.828963, -138.407091, -0.006]
# angles = [1.571584, -0.004266, -0.000046]
# T = create_transformation_matrix(ego_translation, angles)

# print("Homogeneous Transformation Matrix:")
print(transformer.T)
print(transformer.T_inv)

# Another object's coordinates in ego frame (as homogeneous vector)
# object_coords = np.array([3, 4, 1, 1])  # [x, y, z, 1]
object_coords = np.array([4.985880, 112.518, 0.0, 1])
# object_coords = [4.985880, 112.518, 0.0, 1]

# Transform to world frame
world_coords = transformer.apply_transformation(object_coords)
print("\nObject coordinates in world frame:")
print(world_coords[:3])
