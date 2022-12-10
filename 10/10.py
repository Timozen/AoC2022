import pathlib

lines = pathlib.Path("input.txt").read_text().strip().split("\n")


def group_by_n(iterable: list, n: int = 3):
    for i in range(0, len(iterable), n):
        yield iterable[i : i + n]


class Processor:
    def __init__(self) -> None:
        self.register_X = 1
        self.cycle = 0

        self.events = [20, 60, 100, 140, 180, 220]
        self.event_results = []

        self.screen = ["."] * 240
        self.line = 0

    def signal_strength(self):
        self.event_results.append(self.cycle * self.register_X)

    def tick(self):
        if self.register_X - 1 <= self.cycle - self.line * 40 <= self.register_X + 1:
            self.screen[self.cycle] = "#"

        self.cycle += 1
        self.line += self.cycle % 40 == 0

        if self.cycle in self.events:
            self.signal_strength()

    def draw_crt(self):
        for l in group_by_n(self.screen, n=40):
            print("".join(l))

proc = Processor()

for line in lines:
    op, *value = line.split(" ")

    if op == "noop":
        proc.tick()
    elif op == "addx":
        proc.tick()
        proc.tick()
        proc.register_X += int(value[0])

print("Task 1")
print(proc.event_results, sum(proc.event_results))

print("Task 2")
print(proc.draw_crt())
