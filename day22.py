import sys
import re
import collections
import operator
import math

from timeit import default_timer as timer


def parse_input_data(input_data=None):
    data = collections.defaultdict(int)

    if input_data == 'test':
        data[(-1, 0)] = STATE.INFECTED
        data[(1, 1)] = STATE.INFECTED

    else:
        with open('inputs/day22_input.txt', 'r') as f:
            x_pos = -12
            y_pos = 12
            for line in f:
                for char in line:
                    if char == '#':
                        data[(x_pos, y_pos)] = STATE.INFECTED
                    x_pos += 1
                y_pos -= 1
                x_pos = -12

    return data


class STATE(object):
    CLEAN = 0
    WEAK = 1
    INFECTED = 2
    FLAGGED = 3

    @staticmethod
    def advance(state):
        return (state + 1) % 4


class DIRS(object):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    @staticmethod
    def turn_left(current_dir):
        return (current_dir + 1) % 4

    @staticmethod
    def turn_right(current_dir):
        return (current_dir - 1) % 4

    @staticmethod
    def walk(walk_dir, pos):
        if walk_dir == DIRS.UP:
            new_pos = tuple_add(pos, (0, 1))
        elif walk_dir == DIRS.LEFT:
            new_pos = tuple_add(pos, (-1, 0))
        elif walk_dir == DIRS.DOWN:
            new_pos = tuple_add(pos, (0, -1))
        elif walk_dir == DIRS.RIGHT:
            new_pos = tuple_add(pos, (1, 0))
        else:
            raise ValueError("Unknown direction")

        return new_pos


def tuple_add(a, b):
    # print ("{} + {} = {}").format(a, b, tuple(map(operator.add, a, b)))
    return tuple(map(operator.add, a, b))


def execute_step(status_map, current_pos, current_facing):
    did_infect = False
    new_facing = current_facing

    current_state = status_map[current_pos]
    new_state = STATE.advance(current_state)

    if current_state == STATE.CLEAN:
        new_facing = DIRS.turn_left(current_facing)
        status_map[current_pos] = STATE.WEAK
    elif current_state == STATE.WEAK:
        status_map[current_pos] = new_state
        did_infect = True
    elif current_state == STATE.INFECTED:
        new_facing = DIRS.turn_right(current_facing)
        status_map[current_pos] = new_state
    elif current_state == STATE.FLAGGED:
        new_facing = DIRS.turn_right(DIRS.turn_right(current_facing))
        del status_map[current_pos]
    else:
        raise ValueError('Unknown State')

    new_pos = DIRS.walk(new_facing, current_pos)

    return new_pos, new_facing, did_infect


infected_nodes = collections.defaultdict(int)

# infected_nodes = parse_input_data('test')
infected_nodes = parse_input_data()

current_pos = (0, 0)
current_facing = DIRS.UP
infections = 0
last_infection = 0

start = timer()

steps = 10000000
for x in range(steps):
    current_pos, current_facing, did_infect = execute_step(infected_nodes, current_pos, current_facing)
    if did_infect:
        # print (x - last_infection)
        # last_infection = x
        infections += 1

    if x % 1000000 == 0:
        print "{} infections in {} steps".format(infections, x)

# for inf in infected_nodes:
#     print inf

print "{} infections in {} steps".format(infections, steps)

end = timer()
print "Elapsed Time: {}".format(end - start)
