import numpy as np
from scipy.spatial.transform import Rotation as R

    #   Eigen::Vector3f ego_pos(1.828963f, -138.407091f, -0.006f);
    #   Eigen::Vector3f ego_hpr(1.571584f, -0.004266f, -0.000046f);
# Ego position
ego_coords = np.array([1.828963, -138.407091, -0.006])
ego_angles = [1.571584, -0.004266, -0.000046]  # radians

# Create rotation matrix directly
rotation = R.from_euler('zyx', angles, degrees=False)  # 'zyx' = yaw-pitch-roll
rot_matrix = rotation.as_matrix()

print("Rotation Matrix:")
print(rot_matrix)

# Object coordinates in ego frame
object_coords = np.array([4.985880, 112.518, 0.0])

# Transform to world frame
world_coords = rot_matrix @ object_coords + ego_coords
print("\nObject coordinates in world frame:")
print(world_coords)