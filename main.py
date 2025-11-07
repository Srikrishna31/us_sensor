
from ultrasonic_sensor_objects import UltrasonicSensor, Obstacle, EGO
import re
import numpy as np

def read_obstacles_from_file(file_path):
    obstacles = []
    with open(file_path, 'r') as file:
        text = file.read()
    # find all numbers (ints or floats)
    nums = re.findall(r'-?\d+\.?\d*', text)
    nums = [float(n) for n in nums]
    # group every 6 numbers -> obstacle
    groups = [nums[i:i+6] for i in range(0, len(nums), 6) if len(nums[i:i+6])==6]
    for i, g in enumerate(groups):
        obstacles.append(Obstacle(g[0], g[1], g[2], g[3], g[4], g[5], ID=f"obs_{i}"))
    return obstacles

def read_sensors_from_file(file_path):
    sensors = []
    with open(file_path, 'r') as file:
        text = file.read()
    # find all UltrasonicSensor(...) occurrences
    items = re.findall(r'UltrasonicSensor\((.*?)\)', text, re.S)
    for idx, item in enumerate(items):
        # separate name=... if present
        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', item)
        ID = name_match.group(1) if name_match else f"sensor_{idx}"
        # remove any named params, keep only leading numeric args
        left = re.split(r'name\s*=', item)[0]
        nums = re.findall(r'-?\d+\.?\d*', left)
        nums = [float(n) for n in nums]
        if len(nums) >= 6:
            x,y,z,h,p,r = nums[:6]
            sensors.append(UltrasonicSensor(x, y, z, h, p, r, ID=ID))
    return sensors

def main():
    sensors = read_sensors_from_file(r'.\TEST\12sensors.txt')
    print(f"Loaded {len(sensors)} sensors.")
    obstacles = read_obstacles_from_file(r'.\TEST\10obstacles.txt')
    print(f"Loaded {len(obstacles)} obstacles.")

    ego_car = EGO(position_x=0, position_y=0, position_z=0, h=0, p=0, r=0) # # needs to be set properly
    for j, obstacle in enumerate(obstacles):
        obstacle_in_ego = ego_car.transform_from_outside_world_to_car_reference(obstacle)
        print(f"Obstacle {j} ({obstacle.ID}) in EGO frame: {obstacle_in_ego}")
        for i, sensor in enumerate(sensors):
            sensor_point = sensor.transform_from_car_to_sensor_reference(obstacle_in_ego)
            print(f"  Sensor {i} ({sensor.ID}) sees obstacle at: {sensor_point}")
            
            

if __name__ == "__main__":
    main()
