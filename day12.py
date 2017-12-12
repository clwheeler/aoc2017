import sys
import collections

input_map = dict()

# parse input data
with open('inputs/day12_input.txt', 'r') as f:
    for line in f:
        row_data = line.split('<->')
        destinations = row_data[1].split(',')
        input_map[int(row_data[0].strip())] = [int(num) for num in destinations]

groups = []

def traverse_from(start, visited_nodes):
    visited_nodes.add(start)
    destinations = input_map[start]
    for node in destinations:
        if node not in visited_nodes:
            traverse_from(node, visited_nodes)

for node in input_map.iterkeys():
    skip_node = False
    for group in groups:
        if node in group:
            skip_node = True
    if not skip_node:
        visited_nodes = set()
        groups.append(visited_nodes)
        traverse_from(node, visited_nodes)

print len(groups[0])
print len(groups)


