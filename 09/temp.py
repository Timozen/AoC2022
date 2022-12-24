# Part 1 + 2
def move_rope_with_n_knots(num_knots, is_test=False):
    direction_map = {'U': [0, 1], 'D': [0, -1], 'R': [1, 0], 'L': [-1, 0]}
    directions_to_follow = get_directions(is_test)
    knot_positions = {i: [0, 0] for i in range(num_knots)}
    positions_traced_by_tail = set()

    for dir, num_moves in directions_to_follow:
        x_inc, y_inc = direction_map[dir]
        for _ in range(num_moves):
            # move rope head
            head_pos = knot_positions[0]
            head_pos[0], head_pos[1] = head_pos[0] + x_inc, head_pos[1] + y_inc
            knot_positions[0] = head_pos
            # move the individual knots following the head
            for knot_num in range(1, num_knots):
                prev_knot_pos = knot_positions[knot_num - 1]
                curr_knot_pos = knot_positions[knot_num]
                update_rope_knot_pos(prev_knot_pos, curr_knot_pos)
                knot_positions[knot_num] = curr_knot_pos
            # add tail position to positions traced
            tail_pos = knot_positions[num_knots - 1]
            positions_traced_by_tail.add((tail_pos[0], tail_pos[1]))

    return len(positions_traced_by_tail)

# this function updates the position of tail, which is a knot that directly follows head
def update_rope_knot_pos(head_pos, tail_pos):
    # case where head and tail are at same position or are adjacent, don't do anything
    if head_pos == tail_pos or is_adjacent(head_pos, tail_pos):
        return
    else:
        head_x, head_y = head_pos
        tail_x, tail_y = tail_pos
        
        # move tail horizontally
        if abs(head_x - tail_x) == 2 and head_y == tail_y:
            tail_pos[0], tail_pos[1] = tail_x + sign(head_x - tail_x), tail_y
        # move tail vertically
        elif head_x == tail_x and abs(head_y - tail_y) == 2:
            tail_pos[0], tail_pos[1] = tail_x, tail_y + sign(head_y - tail_y)
        # move tail diagonally case 1
        elif abs(head_x - tail_x) == 1 and abs(head_y - tail_y) == 2:
            tail_pos[0], tail_pos[1] = head_x, tail_y + sign(head_y - tail_y)
        # move tail diagonally case 2
        elif abs(head_x - tail_x) == 2 and abs(head_y - tail_y) == 1:
            tail_pos[0], tail_pos[1] = tail_x + sign(head_x - tail_x), head_y
        # move tail diagonally case 3
        elif abs(head_x - tail_x) == 2 and abs(head_y - tail_y) == 2:
            tail_pos[0], tail_pos[1] = tail_x + sign(head_x - tail_x), tail_y + sign(head_y - tail_y)

def sign(x):
    return 1 if x >= 0 else -1

def is_adjacent(pos1, pos2):
    # diagonally adjacent
    if abs(pos1[0] - pos2[0]) == 1 and abs(pos1[1] - pos2[1]) == 1:
        return True
    # horizontally adjacent
    elif abs(pos1[0] - pos2[0]) == 1 and pos1[1] == pos2[1]:
        return True
    # vertically adjacent
    elif pos1[0] == pos2[0] and abs(pos1[0] - pos2[0]) == 1:
        return True
    else:
        return False

def get_directions(is_test=False):
    input_file = "day9_test.txt" if is_test else "input.txt"
    lines = open(input_file, 'r').read().splitlines()
    directions = [(line.split()[0], int(line.split()[1])) for line in lines]
    return directions
    
# Part 1
print(move_rope_with_n_knots(num_knots=2))

# Part 2
print(move_rope_with_n_knots(num_knots=10))