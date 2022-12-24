import pathlib
import functools
import time

# one minute to open a dst_tunnel and one minute to go to the next tunnel
# task 1: most pressure that can be realeased!
lines = pathlib.Path('input.txt').read_text().splitlines()

tunnels = {}

for line in lines:
    first, second = line.split(';')

    current_tunnels = first.split(' ')[1]
    flow_rate = first.split('=')[-1]

    targets = second.replace(",", "").split(' ')[5:]
  
    tunnels[current_tunnels] = {
        "rate" : int(flow_rate),
        "connected_tunnels" : targets
    }  


@functools.cache
def search(visited_tunnels, remaining_minutes, current_tunnel, with_elephant=False):
    if remaining_minutes <= 0:
        if with_elephant:
            return search(visited_tunnels, 26, "AA")
        return 0

    best = 0
    src_tunnel = tunnels[current_tunnel]

    for dst_tunnel in src_tunnel["connected_tunnels"]:
        best = max(best, search(visited_tunnels, remaining_minutes - 1, dst_tunnel, with_elephant=with_elephant))

    if current_tunnel not in visited_tunnels and src_tunnel["rate"] > 0 and remaining_minutes > 0:
        visited_tunnels = set(visited_tunnels)
        visited_tunnels.add(current_tunnel)
        
        remaining_minutes -= 1
        new_sum = remaining_minutes * src_tunnel["rate"]

        for dst_tunnel in src_tunnel["connected_tunnels"]:
            best = max(
                best,
                new_sum + search(frozenset(visited_tunnels), remaining_minutes - 1, dst_tunnel, with_elephant=with_elephant),
            )

    return best

t1 = time.time()
r1 = search(visited_tunnels=frozenset(), remaining_minutes=30, current_tunnel="AA", with_elephant=False)
t2 = time.time() - t1
print(f"Task 1: [{t2}s]", r1)

t1 = time.time()
r2 = search(visited_tunnels=frozenset(), remaining_minutes=26, current_tunnel="AA", with_elephant=True)
t2 = time.time() - t1
print(f"Task 2: [{t2}s]", r2)
