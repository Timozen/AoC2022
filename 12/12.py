from __future__ import annotations

import dataclasses
import string
import pathlib

from collections import deque

import numpy as np

# heights from a to z
# S current Position (a)
# E best position (z)

# reach E in as few steps as possible
# only move U,D,L,R and maximum one height difference!
# compute fewest steps!

height_map_ascii = pathlib.Path("input.txt").read_text().split("\n")
height_map_ascii = [list(hm) for hm in height_map_ascii]
height_map = np.zeros((len(height_map_ascii), len(height_map_ascii[0])), dtype=np.int32)

@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int
    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y
    
    def nb(self) -> list[Point]:
        return [
            Point(self.x + 1, self.y),
            Point(self.x - 1, self.y),
            Point(self.x, self.y + 1),
            Point(self.x, self.y - 1)
        ]
    
    def __repr__(self) -> str:
        return f"[{self.x:2d},{self.y:2d}]"

@dataclasses.dataclass
class Score:
    idx: int
    val: int
    
start = None
target = None

shape = height_map.shape

for i in range(shape[0]):
    for j in range(shape[1]):
        ascii_sym = height_map_ascii[i][j]
        if ascii_sym == "S":
            start = Point(i, j)
            height_map[i,j] = string.ascii_letters.index("a")
        elif ascii_sym == "E":
            target = Point(i, j)
            height_map[i,j] = string.ascii_letters.index("z")
        else:
            height_map[i,j] = string.ascii_letters.index(ascii_sym)



def search(start: Point, target=Point) -> int:
    visited_points = set([start])
    to_visit = deque([(start, 0)])
    
    while to_visit:
        point, dist = to_visit.popleft()
        
        if point == target:
            return dist

        # directions
        for next_point in point.nb():
            if 0 <= next_point.x < shape[0] and 0 <= next_point.y < shape[1]:
                if height_map[next_point.x, next_point.y] == 25 and 25 - height_map[point.x, point.y] <= 1:
                    to_visit.append((next_point, dist+1))
                elif height_map[next_point.x, next_point.y] != 25 and next_point not in visited_points and (height_map[next_point.x, next_point.y] - height_map[point.x, point.y]) <= 1:
                    visited_points.add(next_point)
                    to_visit.append((next_point, dist+1))

print("Start", start)
print("Target", target)

print("Task 1", search(start=start, target=target))

# get all possible a locations
locs = np.unravel_index(np.argwhere(height_map == 0), shape=shape)[1]

scores = []
for x, y in locs:
    d = search(start=Point(x,y), target=target)
    if d:
        scores.append(d)

print("Task 1", min(scores))
