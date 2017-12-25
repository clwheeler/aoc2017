import sys
import re
import collections
import operator
import math

from timeit import default_timer as timer


test_input = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
"""

def parse_input_data(input_data=None):
    data = []

    if input_data:
        for line in input_data.splitlines():
            data.append([int(val) for val in line.strip().split('/')])
        print data
        return data

    with open('inputs/day24_input.txt', 'r') as f:
        for line in f:
            data.append([int(val) for val in line.split('/')])

    return data

# returns all elems that could match
def find_elems_with(value, link_data):
    results = []
    for link in link_data:
        if value in link:
            results.append(link)

    return results


# returns max bridge strength
def traverse(value, link_data, depth = 0):
    possible_links = find_elems_with(value, link_data)

    strongest_bridge = []
    max_strength = 0

    for link in possible_links:
        this_link_data = list(link_data)
        this_link_data.remove(link)
        this_elem = list(link)
        this_elem.remove(value)
        new_end = this_elem[0]

        this_bridge = traverse(new_end, this_link_data, depth + 1)
        this_bridge = list(link) + this_bridge

        # this is wrong
        this_bridge_strength = sum(this_bridge)
        if this_bridge_strength > max_strength:
            max_strength = this_bridge_strength
            strongest_bridge = this_bridge

    return strongest_bridge

def traverse_max_len(value, link_data, depth = 0):
    possible_links = find_elems_with(value, link_data)

    longest_bridge = []
    max_length = 0
    max_strength = 0

    for link in possible_links:
        this_link_data = list(link_data)
        this_link_data.remove(link)
        this_elem = list(link)
        this_elem.remove(value)
        new_end = this_elem[0]

        this_bridge = traverse_max_len(new_end, this_link_data, depth + 1)
        this_bridge = list(link) + this_bridge

        this_bridge_length = len(this_bridge)

        if this_bridge_length > max_length:
            max_length = this_bridge_length
            longest_bridge = this_bridge
            max_strength = sum(this_bridge)
        elif this_bridge_length == max_length:
            if sum(this_bridge) > max_strength:
                longest_bridge = this_bridge
                max_length = this_bridge_length
                max_strength = sum(this_bridge)

    return longest_bridge


# start = timer()

# link_data = parse_input_data()

# best_bridge = traverse(0, link_data)
# print "Strongest"
# print best_bridge
# print sum(best_bridge)
# print len(best_bridge)

link_data = parse_input_data()

long_bridge = traverse_max_len(0, link_data)

print "Longest"
print long_bridge
print sum(long_bridge)
print len(long_bridge)

# end = timer()
# print "Elapsed Time: {}".format(end - start)
