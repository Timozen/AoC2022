import pathlib
import numpy
import itertools

lines = (pathlib.Path(__file__).parent / "input.txt").read_text().split("\n")

groups = [list(map(int, group)) for k, group in itertools.groupby(lines, lambda x: x == "") if not k]

max_1 = max(map(sum, groups))
print("Task 1", max_1)

max_2= sum(sorted(map(sum, groups))[-3:])
print(max_2)