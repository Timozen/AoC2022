from __future__ import annotations
import pathlib
from typing import Union
import sympy

# monkeys yell either a number or a math operation
# find the number of the monkey called root

# the whole input structure is looking like a tree
class Node:
    def __init__(self, name: str, value: Union[int, str] = None):
        self.name = name
        self.value = value
        self.children = []
        
    def add_child(self, child: Node):
        self.children.append(child)
        
    def left_child(self) -> Node:
        return self.children[0]
    
    def right_child(self) -> Node:
        return self.children[1]
        
    def solve(self) -> int:
        if isinstance(self.value, int):
            return self.value
        else:
            if self.value == "+":
                return self.left_child().solve() + self.right_child().solve()
            elif self.value == "*":
                return self.left_child().solve() * self.right_child().solve()
            elif self.value == "-":
                return self.left_child().solve() - self.right_child().solve()
            elif self.value == "/":
                return self.left_child().solve() // self.right_child().solve()
            
    def equation(self, replace_humn: bool = True) -> str:
        if self.name == "humn" and replace_humn:
            return "X"
            
        if isinstance(self.value, int):
            return str(self.value)
        
        return f"({self.left_child().equation()} {self.value} {self.right_child().equation()})"
            
    def find_node(self, name: str) -> Node:
        if self.name == name:
            return self
        else:
            for child in self.children:
                node = child.find_node(name)
                if node is not None:
                    return node
            return None
        
    def is_in_left_subtree(self, node: Node) -> bool:
        if node == self.left_child():
            return True
        else:
            return self.left_child().find_node(node.name) is not None
        
    def is_in_right_subtree(self, node: Node) -> bool:
        return not self.is_in_left_subtree(node)
    
    def solve_left_subtree(self) -> int:
        return self.left_child().solve()
    
    def solve_right_subtree(self) -> int:
        return self.right_child().solve()
            
def get_or_create_node(name: str, node_dict: dict) -> Node:
    if name in node_dict:
        return node_dict[name]
    else:
        node = Node(name)
        node_dict[name] = node
        return node

lines = pathlib.Path('input.txt').read_text().splitlines()

node_dict: dict[str, Node] = {}

for line in lines:
    monkey, instruction = line.split(":")
    instruction = instruction.strip()
    monkey_node = get_or_create_node(monkey, node_dict)
    
    if instruction.isdigit():
        monkey_node.value = int(instruction)
    else:
        # parse the instruction which is two monkeys and an operation
        monkey1, operation, monkey2 = instruction.split(" ")
        
        # check if the monkeys are already in the node_dict        
        monkey_node.value = operation
        monkey_node.add_child(get_or_create_node(monkey1, node_dict))
        monkey_node.add_child(get_or_create_node(monkey2, node_dict))
        

root = node_dict["root"]
print("Task 1:", root.solve())

# Task 2: find the number we have to yell to eualize the root monkey's results
# first we find on which side the "humn" node is, if it is on the left side
# we compute the value of the right subtree
if root.is_in_left_subtree(node_dict["humn"]):
    to_equal_value = root.solve_right_subtree()
    humn_equation  = root.left_child().equation()
else:
    to_equal_value = root.solve_left_subtree()
    humn_equation  = root.right_child().equation()
    
X = sympy.symbols("X")
humn_equation = sympy.simplify(humn_equation)
print("Task 2 Prep:", to_equal_value, "=", humn_equation)
print("Task 2:", sympy.solve(sympy.sympify(humn_equation) - to_equal_value, X)[0])
