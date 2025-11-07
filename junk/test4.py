import numpy as np
from scipy.spatial.transform import Rotation as R

# Given translation and Euler angles (in radians)
translation = np.array([1.828963, -138.407091, -0.006])
euler_angles = np.array([1.571584, -0.004266, -0.000046])  # yaw, pitch, roll

# Create rotation matrix using scipy
rotation = R.from_euler('zyx', euler_angles, degrees=False)
rot_matrix = rotation.as_matrix()

# Build 4x4 homogeneous transformation matrix
T = np.eye(4)
T[:3, :3] = rot_matrix
T[:3, 3] = translation

print("Homogeneous Transformation Matrix:")
print(T)

# Compute inverse for world → ego
T_inv = np.linalg.inv(T)
print("\nInverse Transformation Matrix:")
print(T_inv)

# Example: transform a point from world to ego
world_point = np.array([2.0, -140.0, 0.0, 1.0])  # homogeneous
ego_point = T_inv @ world_point
print("\nWorld → Ego transformed point:")
print(ego_point[:3])