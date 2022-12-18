import pathlib
import numpy as np

lines = pathlib.Path('input.txt').read_text().splitlines()

# the input are x,y,z coordinates inside a big cube
coords = np.array([list(map(int, line.split(','))) for line in lines])

x_max, y_max, z_max = coords.max(axis=0)
cube = np.zeros((x_max + 1, y_max + 1, z_max + 1), dtype=np.int32)

for coord in coords:
    cube[tuple(coord)] = 1

# compute the difference between the cube and shifted versions of itself in all directions
# which is the same as the whole surface of all cubes...
task1 = sum(np.count_nonzero(np.diff(cube, 1, axis=axis_dim, prepend=0, append=0)) for axis_dim in range(3))
print("Task 1:", task1)

# for task 2 do the same but only for the exterior surface
# first get the areas which not filled with the cube
exterior = cube == 0

# assume first every cube is on the outside
outside = np.ones_like(cube) * True
# the outer layers of the cube are cannot be connected to the interior
outside[1:-1, 1:-1, 1:-1] = False

# fill the outside slowly from outside to inside and if there is a cube in the way
# then dont fill there anymore
sum_outside = 0
while True:
    print(sum_outside, outside.sum())
    # store the sum of the exterior to check if it changed
    sum_outside = outside.sum()
    outside_cubes = [np.roll(outside, shift, axis=axis_dim) for axis_dim in range(3) for shift in (-1, 1)]
    # fill the cube inside with the neighbours
    outside = np.logical_and(exterior, np.any(outside_cubes, axis=0))
    if sum_outside == outside.sum():
        break
    
# inverse the filled cube to get the exterior
interior = ~outside
# same as before but now the cube is filled
task2 = sum(np.count_nonzero(np.diff(interior, 1, axis=axis_dim, prepend=0, append=0)) for axis_dim in range(3))
print("Task 2:", task2)

# 3214 is not right too high! way too high ^^ (before adding the outer layers to be false!)
# final answer: 2006