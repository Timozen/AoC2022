from __future__ import annotations
from pathlib import Path

import dataclasses
import numpy as np
import math


@dataclasses.dataclass
class Point:
    x: int
    y: int
    
    def R(self):
        self.x += 1
    
    def L(self):
        self.x -= 1
    
    def U(self):
        self.y += 1
        
    def D(self):
        self.y -= 1
        
    def move(self, dir: str):
        if dir == "R":
            self.R()
        elif dir == "L":
            self.L()
        elif dir == "U":
            self.U()
        elif dir == "D":
            self.D()
        else:
            raise Exception("Screwed up somewhere :^)") 
        
    def dist(self, o: Point):
        x = abs(self.x - o.x)
        y = abs(self.y - o.y)
        return math.sqrt(x*x + y*y)
        
    def set(self, x: int, y:int):
        self.x = x
        self.y = y
        
    def update_in_relation(self, o: Point) -> str:
        # these are basically the update rules for the tail!        
        dist = self.dist(o)
        if dist <= 1.0:
            return
        
        # if dist == math.sqrt(2):
            # diagonal
        
        if dist == 2.0:
            dx = o.x - self.x
            dy = o.y - self.y
            if dx == 2:
                self.set(o.x - 1, self.y)
            elif dx == -2:
                self.set(o.x + 1, self.y)
            elif dy == 2:
                self.set(self.x, o.y - 1)
            elif dy == 2:
                self.set(self.x, o.y + 1)
            return
        
        if dist > 2.0:            
            dx = o.x - self.x
            dy = o.y - self.y
            # .....    .....    .....
            # .....    .....    .....
            # ..H.. -> ...H. -> ..TH.
            # .T...    .T...    .....
            # .....    .....    .....
            if dx == 2 and abs(dy) == 1:
                self.set(o.x - 1, o.y)
            elif dx == -2 and abs(dy) == 1:    
                self.set(o.x + 1, o.y)
            elif dy == 2 and abs(dx) == 1:
                self.set(o.x, o.y - 1)
            elif dy == -2 and abs(dx) == 1:
                self.set(o.x, o.y + 1)


        if dist > 2.5:
            dir_x = int(math.copysign(1, dx))
            dir_y = int(math.copysign(1, dy))
            self.set(o.x - dir_x, o.y - dir_y)
            return


class PlankLength:
    def __init__(self, amount_of_knots, rx, ry) -> None:
        self.knots = [Point(0, 0) for _ in range(amount_of_knots)]
        self.visited_locations = np.zeros((rx, ry), dtype=np.int8)
        self.mark_visited()

    def mark_visited(self):
        k = self.knots[-1]
        self.visited_locations[k.y, k.x] = 1
        
    def draw_visited(self) -> None:
        self.visited_locations = [str(row.tolist()) for row in self.visited_locations]
        lines = []
        for line in self.visited_locations[::-1]:
            lines.append(line)
        print("\n".join(lines), end="\n\n")        
    
    def draw_board(self) -> None:
        char_array = np.chararray(self.visited_locations.shape)
        char_array[:] = '.'
        
        for i in range(1, len(self.knots))[::-1]:
            char_array[self.knots[i].y, self.knots[i].x] = i
        char_array[self.knots[0].y ,self.knots[0].x] = "H"
        
        char_array = [row.tobytes().decode("utf-8") for row in char_array]
        lines = []
        for line in char_array[::-1]:
            lines.append(line)
        print("\n".join(lines), end="\n\n")        
        

    def simulate(self, lines: list[str]) -> None:
        print("== Initial State ==")
        self.draw_board()
        
        for line in lines:
            dir, dir_amt = line.split(" ")
            dir_amt = int(dir_amt)
            print(f"== {dir} {dir_amt} ==")
            for _ in range(dir_amt):
                # move the head
                self.knots[0].move(dir)
                # update the next always in relation of the previous
                for i in range(1, len(self.knots)):
                    self.knots[i].update_in_relation(self.knots[i-1]) 

                self.mark_visited()
                self.draw_board()

    def count_visited(self) -> int:
        return np.sum(self.visited_locations)
        

lines = (Path(__file__).parent / "test2.txt").read_text().split("\n")

rx = 20
ry = 20

pl = PlankLength(amount_of_knots=2, rx=rx, ry=ry)
pl.simulate(lines=lines)

print("Task 1", pl.count_visited())
# print(pl.draw_visited())

pl = PlankLength(amount_of_knots=10, rx=rx, ry=ry)
pl.simulate(lines=lines)

print("Task 2", pl.count_visited())
print(pl.draw_visited())