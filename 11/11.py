from __future__ import annotations

import pathlib
from collections import deque


class Monka:
    def __init__(
        self,
        items: list,
        operator_value: str,
        operator_type: str,
        divider: int,
        target_index_true: int,
        target_index_false: int,
        high_worry: bool
    ) -> None:
        self.items = deque(items)
        self.operator_type = operator_type
        self.divider = divider
        self.target_index_true = target_index_true
        self.target_index_false = target_index_false
        self.high_worry = high_worry
        
        self.worry_operator = 1
        self.inspections = 0
        
        if operator_value == "old":
            self.operator_value = None
        else:
            self.operator_value = int(operator_value)
        
        
    def print_items(self) -> None:
        print(self.items)
        
    def has_items(self) -> bool:
        return len(self.items) != 0
        
    def __rule(self, old_value: int) -> int:
        opv = old_value if self.operator_value is None else self.operator_value
        
        if self.operator_type == "+":
            return old_value + opv
        if self.operator_type == "*":
            return old_value * opv
        
        raise NotImplementedError()
    
    def catch_item(self, new_item:int):
        self.items.append(new_item)

    def next_monka(self) -> tuple[int, int]:
        self.inspections += 1
        
        current_item = self.items.popleft()
        n_value = self.__rule(current_item)
        
        if not self.high_worry:
            n_value //= 3
        else:
            n_value %= self.worry_operator
            
        if n_value % self.divider == 0:
            return self.target_index_true, n_value
        
        return self.target_index_false, n_value
        
    @staticmethod
    def new(text_block: str, high_worry: bool) -> Monka:
        text_block = text_block.strip().split("\n")
        items = list(map(int, text_block[1].split(":")[-1].split(",")))
        
        o_type, o_value = text_block[2].split(" ")[-2:]
        
        divider = int(text_block[3].split(" ")[-1])
        target_index_true  = int(text_block[4].split(" ")[-1])
        target_index_false = int(text_block[5].split(" ")[-1])
        return Monka(
            items=items,
            operator_type=o_type,
            operator_value=o_value,
            divider=divider,
            target_index_true=target_index_true,
            target_index_false=target_index_false,
            high_worry=high_worry
        )
        
def worry_game(lines, rounds, high_worry):
    monkas: list[Monka] = []
    for block in lines:
        monkas.append(Monka.new(text_block=block, high_worry=high_worry))
    
    # 猴子 :^)
    worry_operator = 1
    for monka in monkas:
        worry_operator *= monka.divider
    for monka in monkas:
        monka.worry_operator = worry_operator

    for _ in range(1, rounds+1):
        for monka in monkas:
            while monka.has_items():
                target_idx, n_item = monka.next_monka()
                monkas[target_idx].catch_item(new_item=n_item)

    inspections = [monka.inspections for monka in monkas]
    t1, t2 = sorted(inspections)[-2:]
    return t1, t2, t1*t2

lines = pathlib.Path("input.txt").read_text().split("\n\n")
print("Task 1", worry_game(lines,     20, high_worry=False))
print("Task 2", worry_game(lines, 10_000, high_worry=True))
