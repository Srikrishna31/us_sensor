
from ultrasonic_sensor_objects import UltrasonicSensor, Obstacle, EGO
import re
import numpy as np
from csv_reader import read_sensor_data_from_csv

# import debugpy
# debugpy.listen(("0.0.0.0", 5678))
# print("Waiting for debugger to attach...")
# debugpy.wait_for_client()

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
        obstacles.append(Obstacle(g[0], g[1], g[2], g[3], g[4], g[5], id=f"obs_{i}"))
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
            sensors.append(UltrasonicSensor(ID, x, y, z, h, p, r))
    return sensors

def main():
    sensor_info = read_sensor_data_from_csv()
    # print(sensor_info)
    obstacles = read_obstacles_from_file(r'./TEST/10obstacles.txt')
    print(f"Loaded {len(obstacles)} obstacles.")

    distances = {}
    ego_car = EGO(position_x=0.0, position_y=0.0, position_z=0.0, h=0, p=0, r=0, sensor_data=sensor_info) # # needs to be set properly
    for j, obstacle in enumerate(obstacles):
        obstacle_in_ego = ego_car.transform_from_outside_world_to_car_reference(obstacle)
        # print(f"Obstacle {j} ({obstacle.id}) in EGO frame: {obstacle_in_ego}")
        for i, sensor in enumerate(ego_car.get_sensors()):
            obj_distances = []
            # print(f"Sensor {i} ({sensor.ID})")
            sensor_point = sensor.transform_from_car_to_sensor_reference(obstacle_in_ego)
            # print(sensor_point)
            res, min_d = sensor.detect_obstacle(sensor_point)
            print(f"Res: {res}")
            if res:
                print(f"  Sensor {i} ({sensor.ID}) sees obstacle at: {min_d}")
                # obj_distances.append(res[1][0])
            # else:
            #     print(f"  Sensor {i} ({sensor.ID}) DOESN'T see obstacle at: {sensor_point}.")
            if obj_distances:
                distances[sensor.ID] = min(obj_distances)
                # print(f"  Sensor {i} ({sensor.ID}) sees obstacle at: {sensor_point} with distance: {min(obj_distances)}")


        for d in distances:
            print(f"{d}: {distances[d][0]}")

        # print(f"{distances}")
            

if __name__ == "__main__":
    main()
