import pathlib
import re
import functools
from tqdm import tqdm

@functools.cache
def geodes_bfs(
    robot_e_costs_e: int,
    robot_l_costs_e: int,
    robot_o_costs_e: int,
    robot_o_costs_l: int,
    robot_g_costs_e: int,
    robot_g_costs_o: int,
    robot_e_amount: int,
    robot_l_amount: int,
    robot_o_amount: int,
    robot_g_amount: int,
    e_amount: int,
    l_amount: int,
    o_amount: int,
    time_remaining: int,
) -> int:
    if time_remaining == 0:
        return 0
    
    o_possible = o_amount
    for i in range(0, time_remaining - 2):
        o_possible += robot_o_amount + i
    if o_possible < robot_g_costs_o:
        return robot_g_amount * time_remaining
        
    if robot_g_costs_e <= e_amount and robot_g_costs_o <= o_amount:
        return robot_g_amount + geodes_bfs(
            robot_e_costs_e,
            robot_l_costs_e,
            robot_o_costs_e,
            robot_o_costs_l,
            robot_g_costs_e,
            robot_g_costs_o,
            robot_e_amount,
            robot_l_amount,
            robot_o_amount,
            robot_g_amount + 1,
            e_amount + robot_e_amount - robot_g_costs_e,
            l_amount + robot_l_amount,
            o_amount + robot_o_amount - robot_g_costs_o,
            time_remaining - 1,
        )
           
    # we have four options now here (if we have enough resources)
    # 1. produce no robot
    # 2. produce an ore robot
    # 3. produce a clay robot
    # 4. produce an obsidian robot
    
    options = []
    
    # 1. produce no robot
    options.append(
        geodes_bfs(
            robot_e_costs_e,
            robot_l_costs_e,
            robot_o_costs_e,
            robot_o_costs_l,
            robot_g_costs_e,
            robot_g_costs_o,
            robot_e_amount,
            robot_l_amount,
            robot_o_amount,
            robot_g_amount,
            e_amount + robot_e_amount, 
            l_amount + robot_l_amount,
            o_amount + robot_o_amount,
            time_remaining - 1,
        )
    )
    
    # 2. produce an ore robot
    if robot_e_costs_e <= e_amount:
       options.append(
            geodes_bfs(
                robot_e_costs_e,
                robot_l_costs_e,
                robot_o_costs_e,
                robot_o_costs_l,
                robot_g_costs_e,
                robot_g_costs_o,
                robot_e_amount + 1,
                robot_l_amount,
                robot_o_amount,
                robot_g_amount,
                e_amount + robot_e_amount - robot_e_costs_e, 
                l_amount + robot_l_amount,
                o_amount + robot_o_amount,
                time_remaining - 1,
            )
        ) 
    
    # 3. produce a clay robot
    if robot_l_costs_e <= e_amount:
        options.append(
            geodes_bfs(
                robot_e_costs_e,
                robot_l_costs_e,
                robot_o_costs_e,
                robot_o_costs_l,
                robot_g_costs_e,
                robot_g_costs_o,
                robot_e_amount,
                robot_l_amount + 1,
                robot_o_amount,
                robot_g_amount,
                e_amount + robot_e_amount - robot_l_costs_e, 
                l_amount + robot_l_amount,
                o_amount + robot_o_amount,
                time_remaining - 1,
            )
        ) 
    
    # 4. produce an obsidian robot
    if robot_o_costs_e <= e_amount and robot_o_costs_l <= l_amount:
        options.append(
            geodes_bfs(
                robot_e_costs_e,
                robot_l_costs_e,
                robot_o_costs_e,
                robot_o_costs_l,
                robot_g_costs_e,
                robot_g_costs_o,
                robot_e_amount,
                robot_l_amount,
                robot_o_amount + 1,
                robot_g_amount,
                e_amount + robot_e_amount - robot_o_costs_e, 
                l_amount + robot_l_amount - robot_o_costs_l,
                o_amount + robot_o_amount,
                time_remaining - 1,
            )
        ) 
    
    return robot_g_amount + max(options)

blue_prints = pathlib.Path("input.txt").read_text().splitlines()

task_1 = 0
for bdx, bp in tqdm(enumerate(blue_prints), "Blueprints", total=len(blue_prints)):
    bp_score = 0
    
    bp = bp.split(":")
    ore, clay, obsidian, geode = bp[1].split(".")[:-1]
    
    ore = re.findall(r"\d+", ore)[0]
    clay = re.findall(r"\d+", clay)[0]
    obsidian = re.findall(r"\d+", obsidian)
    geode = re.findall(r"\d+", geode)   
    
    score = geodes_bfs(
        robot_e_costs_e = int(ore),
        robot_l_costs_e = int(clay),
        robot_o_costs_e = int(obsidian[0]),
        robot_o_costs_l = int(obsidian[1]),
        robot_g_costs_e = int(geode[0]),
        robot_g_costs_o = int(geode[1]),
        robot_e_amount = 1,
        robot_l_amount = 0,
        robot_o_amount = 0,
        robot_g_amount = 0,
        e_amount = 0, 
        l_amount = 0,
        o_amount = 0,
        time_remaining = 24,
    )
    
    bp_score += score * (bdx + 1)
    task_1 += bp_score
        
print("Task 1:", task_1)