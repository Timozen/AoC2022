import pathlib
import enum
import re

class Resource(enum.Enum):
    ore = 1
    clay = 2
    obsidian = 3
    geode = 4


class Robot:
    def __init__(self, produce: Resource):
        self.production = produce

    def __call__(self, *_, **__) -> tuple[Resource, int]:
        return self.production, 1

class OreRobot(Robot):
    def __init__(self):
        super().__init__(Resource.ore)
        
class ClayRobot(Robot):
    def __init__(self):
        super().__init__(Resource.clay)
        
class ObsidianRobot(Robot):
    def __init__(self):
        super().__init__(Resource.obsidian)
        
class GeodeRobot(Robot):
    def __init__(self):
        super().__init__(Resource.geode)


class Factory:
    def __init__(self, blueprint_for_costs: dict[str, dict[Resource, int]]):
        self.blueprint_for_costs = blueprint_for_costs
        
        self.inventory = {resource: 0 for resource in Resource}
        self.robots = {resource: [] for resource in Resource}
        self.robots[Resource.ore].append(OreRobot())
        
        self.robot_map = {
            "ore" : OreRobot,
            "clay" : ClayRobot,
            "obsidian" : ObsidianRobot,
            "geode" : GeodeRobot,
        }
                
        
    def tick(self) -> None:
        production_queue = []
        # production phase (resources are used to produce other resources)
        # as we want to produce as many geodes as possible, we start with them as highest priority
        # if we have enough resources to produce a geode, we do so
        for robot_type in ["geode", "obsidian", "clay", "ore"]:
            robot_to_produce = self.blueprint_for_costs[robot_type]
            if all(self.inventory[resource] >= amount for resource, amount in robot_to_produce.items()):
                for resource, amount in robot_to_produce.items():
                    self.inventory[resource] -= amount
                production_queue.append(self.robot_map[robot_type]())
        
        # harvesting phase (robots produce resources)
        for robots in self.robots.values():
            for robot in robots:
                produced_resource, amount = robot()
                self.inventory[produced_resource] += amount

        # deploy phase check if there are new robots ready from the production queue
        for robot in production_queue:
            self.robots[robot.production].append(robot)
     
    def simulate(self, steps: int) -> None:        
        for i in range(1, steps+1):
            self.tick()
            
            # list the amount of robots for each resource
            print(f"Step [{i:2d}]:", end=" ")
            for resource, robots in self.robots.items():
                print(f"{resource.name}: {len(robots)}", end=" ")
            print()


blue_prints = pathlib.Path("test.txt").read_text().splitlines()

for bp in blue_prints:
    bp = bp.split(":")
    ore, clay, obsidian, geode = bp[1].split(".")[:-1]
    
    ore = re.findall(r"\d+", ore)[0]
    clay = re.findall(r"\d+", clay)[0]
    obsidian = re.findall(r"\d+", obsidian)
    geode = re.findall(r"\d+", geode)    
    
    blue_print = {
        "ore": {
            Resource.ore: int(ore), 
        },
        "clay": {
            Resource.ore: int(clay), 
        },
        "obsidian": {
            Resource.ore: int(obsidian[0]), 
            Resource.clay: int(obsidian[1]),
        },
        "geode": {
            Resource.ore: int(geode[0]), 
            Resource.obsidian: int(geode[1]),
        }
    }
    print(blue_print)
    
    fac = Factory(blue_print)
    fac.simulate(24)
    
    produced_geodes = fac.inventory[Resource.geode]
    print(produced_geodes)
    break
    