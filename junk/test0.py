import numpy as np

def rotation_matrix_from_euler(h, p, r):
    """
    Create a rotation matrix from Euler angles (heading, pitch, roll).
    h: heading (yaw) in radians
    p: pitch in radians
    r: roll in radians
    """
    # Rotation about Z-axis (heading/yaw)
    Rz = np.array([
        [np.cos(h), -np.sin(h), 0],
        [np.sin(h), np.cos(h), 0],
        [0, 0, 1]
    ])

    # Rotation about Y-axis (pitch)
    Ry = np.array([
        [np.cos(p), 0, np.sin(p)],
        [0, 1, 0],
        [-np.sin(p), 0, np.cos(p)]
    ])

    # Rotation about X-axis (roll)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(r), -np.sin(r)],
        [0, np.sin(r), np.cos(r)]
    ])

    # Combined rotation matrix: R = Rz * Ry * Rx
    R = Rz @ Ry @ Rx
    return R

# Example usage:
ego_coords = np.array([10, 5, 2])  # Ego position in world frame
heading = np.deg2rad(45)  # 45° yaw
pitch = np.deg2rad(10)    # 10° pitch
roll = np.deg2rad(5)      # 5° roll

# Generate rotation matrix
R = rotation_matrix_from_euler(heading, pitch, roll)

print("Rotation Matrix:")
print(R)

# Another object's coordinates in ego frame
object_coords = np.array([3, 4, 1])

# Convert object's coordinates to world frame
world_coords = R @ object_coords + ego_coords

print("\nObject coordinates in world frame:")
print(world_coords)
