import sys
import re
import collections

from timeit import default_timer as timer

test_input = """     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
"""


def parse_input_data(input_data=None):
    data = []

    if not input_data:
        with open('inputs/day19_input.txt', 'r') as f:
            for line in f:
                data.append([char for char in line])
    else:
        max_len = 0
        for line in input_data.splitlines():
            if len(line) > max_len:
                max_len = len(line)
        for line in input_data.splitlines():
            this_row = [char for char in line]
            while len(this_row) < max_len:
                this_row.append(' ')
            data.append(this_row)

    return data

def tuple_add(a, b):
    return map(sum, zip(a, b))

class DIR(object):
    NORTH = 'n'
    SOUTH = 's'
    EAST = 'e'
    WEST = 'w'

def invert(direction):
    if direction == DIR.NORTH:
        return DIR.SOUTH
    if direction == DIR.SOUTH:
        return DIR.NORTH
    if direction == DIR.EAST:
        return DIR.WEST
    if direction == DIR.WEST:
        return DIR.EAST

# returns next pos, letters
def traverse_tile(last_pos, current_pos):
    current_tile = input_map[current_pos[1]][current_pos[0]]
    delta = (current_pos[0] - last_pos[0], current_pos[1] - last_pos[1])
    next_pos = tuple_add(current_pos, delta)
    letter = None

    if current_tile == '+':
        for next_dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if next_dir in [(0, 1), (0, -1)]:
                invalid_next = ['-', ' ']
            else:
                invalid_next = ['|', ' ']

            next_dir_pos = tuple_add(current_pos, next_dir)
            # don't go backwards
            if next_dir_pos[0] == last_pos[0] and next_dir_pos[1] == last_pos[1]:
                continue
            # OOB

            if next_dir_pos[1] < 0 or next_dir_pos[1] > len(input_map) - 1:
                continue
            if next_dir_pos[0] < 0 or next_dir_pos[0] > len(input_map[next_dir_pos[1]]) - 1:
                continue

            next_tile = input_map[next_dir_pos[1]][next_dir_pos[0]]
            if next_tile in invalid_next:
                continue

            next_pos = next_dir_pos
            break

    elif current_tile in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        # stop if we're at the end
        if delta in [(0, 1), (0, -1)]:
            invalid_next = ['-', ' ']
        else:
            invalid_next = ['|', ' ']

        next_tile = input_map[next_pos[1]][next_pos[0]]
        if next_tile in invalid_next:
            next_pos = current_pos

        letter = current_tile

    return next_pos, letter

def traverse_map(input_map):
    steps = 0
    current_pos = (input_map[0].index('|'), 0)
    last_pos = (input_map[0].index('|'), -1)
    current_tile = input_map[current_pos[1]][current_pos[0]]
    all_letters = []

    HALT = False

    while not HALT:
        current_tile = input_map[current_pos[1]][current_pos[0]]
        # print "{}: {}".format(current_pos, current_tile)
        letter = None
        new_pos, letter = traverse_tile(last_pos, current_pos)
        last_pos = current_pos
        current_pos = new_pos

        if letter:
            all_letters = all_letters + [letter]

        if last_pos == current_pos:
            HALT = True
        steps += 1

    print steps
    print "letters: {}".format("".join(all_letters))

# start = timer()

input_map = parse_input_data(test_input)
traverse_map(input_map)

input_map = parse_input_data()
traverse_map(input_map)


# end = timer()
# print "Elapsed Time: {}".format(end - start)
