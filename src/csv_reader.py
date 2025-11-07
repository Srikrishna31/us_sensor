import math
import csv

def read_sensor_data_from_csv(file_path = "data/sensors.csv"):
    sensor_dict = {}
    with open(file_path, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized_row = {k.strip(): v.strip() for k, v in row.items()}
            sensor = normalized_row['Sensor']
            sensor_dict[sensor] = {
                'X_m': float(normalized_row['X in mm']) / 1000,
                'Y_m': float(normalized_row['Y in mm']) / 1000,
                'Z_m': float(normalized_row['Z in mm']) / 1000,
                'roll_rad': math.radians(float(normalized_row['roll in deg'])),
                'pitch_rad': math.radians(float(normalized_row['pitch in deg'])),
                'yaw_rad': math.radians(float(normalized_row['yaw in deg']))
            }
    return sensor_dict
