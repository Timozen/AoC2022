import copy
import itertools
import pathlib


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

lines = pathlib.Path('input.txt').read_text().splitlines()

beacons = {}
distances = {}

for line in lines:
    sensor, beacon = line.split(":")
    sensor_x, sensor_y = map(int, sensor[10:].replace("x=", "").replace("y=", "").split(","))
    beacon_x, beacon_y = map(int, beacon[22:].replace("x=", "").replace("y=", "").split(","))
    sensor = (sensor_x, sensor_y)
    beacon = (beacon_x, beacon_y)
    
    beacons[sensor] = beacon
    distances[sensor] = manhattan_distance(sensor, beacon)
    
min_x = int(min([k[0] - d for k, d in distances.items()]))
max_x = int(max([k[0] + d for k, d in distances.items()]))

sensors = set(beacons.values()) | set(beacons.keys())

beacon_free = 0
beacon_row = 2_000_000

for x in range(min_x, max_x + 1):    
    if any(abs(s[0] - x) + abs(s[1] - beacon_row) <= d and (x, beacon_row) not in sensors for s, d in distances.items()):
        beacon_free += 1

print("Task 1:", beacon_free)

max_range = 4_000_000
frequency_tune = 4_000_000
sensor_covered = [[] for _ in range(max_range + 1)]

for sensor, distance in distances.items():
    half = list(range(0, distance + 1))
    
    sensor_rangey = range(sensor[1] - distance, sensor[1] + distance + 1)
    mirrored_half = half + list(reversed(half[:-1]))
    
    for y, x in zip(sensor_rangey, mirrored_half):
        if not (0 <= y <= max_range):
            continue
        sensor_covered[y].append((sensor[0] - x, sensor[0] + x + 1))

def shrink_down(interval_0: tuple[int, int], interval_1: tuple[int, int]) -> tuple[int, int]:
    start_0, end_0 = interval_0
    start_1, end_1 = interval_1
    
    # find the range covered by both intervals
    area_interval = sorted([start_0, end_0, start_1, end_1])
    
    new_intervals = []
    if area_interval[0] == start_0 and area_interval[1] != start_0:
        new_intervals.append((area_interval[0], area_interval[1]))
    if area_interval[3] == end_0 and area_interval[2] != end_0:
        new_intervals.append((area_interval[2], area_interval[3]))
    return new_intervals


interesting_range = [[0, max_range + 1]]
for y, covered in enumerate(sensor_covered):
    scan_range = copy.deepcopy(interesting_range)
    # print(y, covered)
    for cover in covered:
        # print(y, 1, pos, scan_range)
        scan_range = list(itertools.chain(*[shrink_down(remaining_range, cover) for remaining_range in scan_range]))
        # print(y, 2, pos, scan_range)
            
    if scan_range:
        x = scan_range[0][0]
        print("Task 2:", x * frequency_tune + y)
        break
    
    #13_213_086_906_101