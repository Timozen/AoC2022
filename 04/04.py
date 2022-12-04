from __future__ import annotations

import pathlib

lines = (pathlib.Path(__file__).parent / "input.txt").read_text().strip().split("\n")
# Task 1
class Interval:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end
        
    def includes(self, other: Interval) -> bool:        
        return self.start <= other.start and  other.end <= self.end
    
    def overlaps(self, other: Interval) -> bool:
        return (
            other.start <= self.start <= other.end
            or
            other.start <= self.end <= other.end
        )
    
    def __and__(self, o: Interval) -> bool:
        return self.includes(o) or o.includes(self)
    
    def __or__(self, o: Interval) -> bool:
        return self.overlaps(o) or o.overlaps(self)    
    
    def __repr__(self) -> str:
        return f"[{self.start:2d},{self.end:2d}]"
    
    @staticmethod
    def new(line_input: str) -> Interval:
        start, end = line_input.split("-")
        # dont forget to convert them to ints...
        return Interval(int(start), int(end))

including_interval_count = 0
for line in lines:
    interval1, interval2 = map(Interval.new, line.split(','))
    including_interval_count += interval1 & interval2
    print(interval1, interval2, interval1 & interval2)

# has to be higher than 503 :^) and lower than 575 and in the end 538
print("Task 1", including_interval_count)
    
# Task 2
overlapping_interval_count = 0
for line in lines:
    interval1, interval2 = map(Interval.new, line.split(','))
    overlapping_interval_count += interval1 | interval2
    print(interval1, interval2, interval1 | interval2)
print("Task 2", overlapping_interval_count)
    