import pathlib
import numpy as np

rocks = [
    np.array([[1, 1, 1, 1]], dtype=bool),
    np.array([[0, 1, 0],[1, 1, 1],[0, 1, 0]], dtype=bool),
    np.array([[1, 1, 1],[0, 0, 1],[0, 0, 1]], dtype=bool),
    np.array([[1],[1],[1],[1]], dtype=bool),
    np.array([[1, 1],[1, 1]], dtype=bool),
]
class Tetris:
    def __init__(self, gas_dirs: str):
        self.grid = np.zeros((10_000, 7), dtype=bool)
        self.current_rock_idx = 0
        self.last_row_with_stone = 0
        self.rocks_placed = 0
        self.gas_dirs = [c=='>' for c in gas_dirs]
        self.current_gas_idx = 0
    
    def gas_from_left(self):
        temp_index = self.current_gas_idx
        self.current_gas_idx = (self.current_gas_idx+1) % len(self.gas_dirs)
        return self.gas_dirs[temp_index]

    def compute_hash(self):
        # hash is combination from the last row and which cycles the stones and gases are!
        str_hash = ""
        str_hash += str(self.current_gas_idx)
        str_hash += str(self.current_rock_idx)
        str_hash += str(self.grid[self.last_row_with_stone].tolist())
        return str_hash

    def check_collision(self, x: int, y: int):
        rock = rocks[self.current_rock_idx]
        h, w = rock.shape
        return np.any(np.logical_and(self.grid[y:y+h,x:x+w], rock))

    def set_stone(self, x, y):
        rock = rocks[self.current_rock_idx]
        self.rocks_placed += 1
        self.current_rock_idx = (self.current_rock_idx+1)%len(rocks)
        
        h, w = rock.shape
        self.grid[y:y+h,x:x+w] = np.logical_or(self.grid[y:y+h,x:x+w], rock)

        # check if we need to move up in our last row
        while self.grid[self.last_row_with_stone].any():
            self.last_row_with_stone+=1

    def move_rock(self, prints = False):
        rock = rocks[self.current_rock_idx]
        x = 2
        _, w = rock.shape
        y = self.last_row_with_stone + 3
        while True:
            if prints:
                self.print_to_cmd(x,y)
            if self.gas_from_left():
                if x + w < 7 and not self.check_collision(x + 1, y):
                    x += 1
            else:
                if x > 0  and not self.check_collision(x - 1, y):
                    x -= 1
            if y > 0 and not self.check_collision(x, y - 1):
                y -= 1
            else:
                self.set_stone(x, y)
                return

    
    def print_to_cmd(self,x,y):
        rock = rocks[self.current_rock_idx]
        h,w = rock.shape
        tmp = np.copy(self.grid)
        tmp[y:y+h, x:x+w] = np.logical_or(tmp[y:y+h, x:x+w], rock)
       
        for row in tmp:
            for v in row:
                print("#" if v else ".", end="")
            print()

input = pathlib.Path("input.txt").read_text()    

p1 = p2 = 0
grid = Tetris(input.strip())
saw_hash = False
hash_val = 0

for round in range(2022):
    grid.move_rock()
p1 = grid.last_row_with_stone

round += 1
while round < 1000000000000:
    grid.move_rock()
    if saw_hash == False:
        if hash:= grid.compute_hash():
            saw_hash = True
            cycle_height = grid.last_row_with_stone
            cycle_placed = grid.rocks_placed
            hash_val = hash
    else:
        if grid.compute_hash() == hash_val:
            dh = grid.last_row_with_stone - cycle_height
            dp = grid.rocks_placed - cycle_placed
            cycle_apperance = (1000000000000 - round) // dp
            round += dp * cycle_apperance
            p2 += dh * cycle_apperance
    round+=1

p2 += grid.last_row_with_stone

print("Task 1:", p1)
print("Task 2:", p2)

