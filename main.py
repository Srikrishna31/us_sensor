
from Objects import UltrasonicSensor, Obstacle, EGO, calculate_3d_distance


def read_obstacles_from_file(file_path):
    obstacles = []
    with open(file_path, 'r') as file:
        for line in file:
            data = tuple(map(int, line.strip().split(',')))
            obstacles.append(Obstacle(*data))
    return obstacles

def main():
    sensors = [UltrasonicSensor() for _ in range(12)]

    obstacles = read_obstacles_from_file(r'.\TEST\10obstacles.txt')
    print(obstacles)

    # Create one EGO car
    ego_car = EGO(position_x=0, position_y=0, position_z=0)

    for i, sensor in enumerate(sensors):
        for j, obstacle in enumerate(obstacles):
            distance = calculate_3d_distance(sensor, obstacle)
            print(f"Distance from Sensor {i} to Obstacle {j}: {distance:.2f} cm")
            

if __name__ == "__main__":
    main()
