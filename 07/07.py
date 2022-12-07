from __future__ import annotations

import dataclasses
import pathlib
from collections import deque
from typing import Optional


@dataclasses.dataclass
class FileNode:
    name: str
    size: int
    
class DirNode:
    def __init__(self, name: str, parent: Optional[DirNode] = None) -> None:
        self.name = name
        self.parent = parent
        
        self.sub_nodes : list[DirNode] = []
        self.files : list[FileNode] = []
        
    def add_subnodes(self, name: str) -> DirNode:
        sub_node = DirNode(name, parent=self)
        self.sub_nodes.append(sub_node)
        return sub_node
    
    def add_file(self, file: FileNode) -> None:
        self.files.append(file)
    
    def get_size(self) -> int:
        size = sum(map(lambda file: file.size, self.files))
        size += sum(map(lambda node: node.get_size(), self.sub_nodes))
        return size
    

lines = (pathlib.Path(__file__).parent / "input.txt").read_text().split("\n")

possible_stacks: deque[DirNode] = deque()
directories: list[DirNode] = []


for line in lines:
    line = line.strip()
    if line.startswith("$"):
        _, *cmd = line.split()

        if len(cmd) == 1: #ls
            continue
        if len(cmd) == 2:
            if cmd[-1] == "..":
                possible_stacks.popleft()
            else:
                if len(possible_stacks) == 0:
                    directory = DirNode(name=cmd[-1])
                else:
                    directory = possible_stacks[0].add_subnodes(name=cmd[-1])
                possible_stacks.appendleft(directory)
                directories.append(directory)
    else:
        info, name = line.split()
        if info == "dir":
            continue
            
        file = FileNode(name, size=int(info))
        possible_stacks[0].add_file(file=file)
        
        
sizes = [d.get_size() for d in directories]
part_1 = sum(s for s in sizes if s <= 100000)

print("Task 1", part_1)

root = directories[0]
required = 30000000 - (70000000 - root.get_size())
mapping = [(d.get_size(), d.name) for d in directories if d.get_size() >= required]
part_2 = min(mapping)[0]

print("Task 2", part_2)