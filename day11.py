import sys
import collections

input_string = ''

# parse input data
with open('inputs/day11_input.txt', 'r') as f:
    for line in f:
        input_string = line


def tuple_add(a, b):
    return map(sum, zip(a, b))

def hex_distance(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])) / 2

# n = +y, 0x
# ne = +x, 0y
# s = +z, 0x
# see: https://www.redblobgames.com/grids/hexagons/
def navigate(pos, direction):
    if direction == 'n':
        return tuple_add(pos, (0, 1, -1))
    if direction == 'ne':
        return tuple_add(pos, (1, 0, -1))
    if direction == 'nw':
        return tuple_add(pos, (-1, 1, 0))
    if direction == 's':
        return tuple_add(pos, (0, -1, 1))
    if direction == 'se':
        return tuple_add(pos, (1, -1, 0))
    if direction == 'sw':
        return tuple_add(pos, (-1, 0, 1))


pos = (0,0,0)
max_distance = 0
for move in input_string.strip().split(','):
    pos = navigate(pos, move)
    max_distance = max(max_distance, hex_distance(pos, (0, 0, 0)))

print hex_distance(pos, (0, 0, 0))
print max_distance
