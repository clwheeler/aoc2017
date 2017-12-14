import sys
import collections

instructions = []
registers = collections.defaultdict(int)

# test_inst = [
# "b inc 5 if a > 1",
# "a inc 1 if b < 5",
# "c dec -10 if a >= 1",
# "c inc -20 if c == 10",
# ]

# parse input data
with open('inputs/day8_input.txt', 'r') as f:
    for line in f:
        instructions.append(line.strip().split(' '))

# for line in test_inst:
#     instructions.append(line.strip().split(' '))


def get_comp_operator(code):
    if code == '==':
        return lambda x, y: x == y
    elif code == '!=':
        return lambda x, y: x != y
    elif code == '>':
        return lambda x, y: x > y
    elif code == '>=':
        return lambda x, y: x >= y
    elif code == '<':
        return lambda x, y: x < y
    elif code == '<=':
        return lambda x, y: x <= y


def get_operator(instruction):
    if instruction == 'inc':
        return lambda a, b: a + b
    else:
        return lambda a, b: a - b

max_value = 0

for this_inst in instructions:
    reg = this_inst[0]
    current_value = registers[reg]

    operator = get_operator(this_inst[1])
    comp_operator = get_comp_operator(this_inst[5])

    if comp_operator(registers[this_inst[4]], int(this_inst[6])):
        registers[reg] = operator(registers[reg], int(this_inst[2]))
        if registers[reg] > max_value:
            max_value = registers[reg]

final_max = max(registers.itervalues())
print "final_max: {}".format(final_max)
print "max: {}".format(max_value)
