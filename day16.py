import sys
import re
import collections

from timeit import default_timer as timer

input_data = []
# parse input data
with open('inputs/day16_input.txt', 'r') as f:
    for line in f:
        step_data = line.strip().split(',')
        for step in step_data:
            inst = step[0]
            partners = step[1:].split('/')
            partners.append(0)
            try:
                partners[0] = int(partners[0])
                partners[1] = int(partners[1])
            except Exception as e:
                pass
            input_data.append((inst, partners[0], partners[1]))


class DANCE_STEP(object):
    SPIN = 's'
    EXCHANGE = 'x'
    PARTNER = 'p'


def run_permutation_dance(dance_steps, num_members, current_order=None):
    if not current_order:
        current_order = collections.deque()
        for code in range(97, 97 + num_members):
            current_order.append(chr(code))

    for step in dance_steps:
        instruction = step[0]
        if instruction == DANCE_STEP.SPIN:
            spin_length = step[1]
            current_order.rotate(spin_length)
        elif instruction == DANCE_STEP.EXCHANGE:
            p = current_order[step[1]]
            current_order[step[1]] = current_order[step[2]]
            current_order[step[2]] = p
        elif instruction == DANCE_STEP.PARTNER:
            partners = [0, 0]
            for pos in range(len(current_order)):
                if current_order[pos] == step[1]:
                    partners[0] = pos
                if current_order[pos] == step[2]:
                    partners[1] = pos
            p = current_order[partners[0]]
            current_order[partners[0]] = current_order[partners[1]]
            current_order[partners[1]] = p
        else:
            print 'ERROR'

    return current_order

start = timer()

# print "Test Run"
# print ''.join(run_permutation_dance(['s1', 'x3/4', 'pe/b'], 5, None))
print "Part A"
print ''.join(run_permutation_dance(input_data, 16, None))

print "Part B"
order = None
all_orders = []

# dance has a period of 24
# 1000000000 % 24 = 16
for i in range(16):
    order = run_permutation_dance(input_data, 16, order)
    this_order = ''.join(order)
    print this_order


# 536870912 =

end = timer()
print "Elapsed Time: {}".format(end - start)
