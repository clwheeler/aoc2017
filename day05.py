import sys

# steps = 0
# instructions = [0, 3, 0, 1, -3]
# visits = [0, 0, 0, 0, 0]
instructions = []
visits = []

with open('inputs/aocday5_input.txt', 'r') as f:
    for line in f:
        instructions.append(int(line))
        visits.append(0)

def visit(index):
    offset = instructions[index] + visits[index]
    newPos = index + offset
    if offset >= 3:
        visits[index] = visits[index] - 1
    else:
        visits[index] = visits[index] + 1
    # print "index {} + {} = {}".format(index, offset, newPos)
    return newPos

currentPos = 0
steps = 0

while True:
    try:
        currentPos = visit(currentPos)
    except:
        print steps
        break
    steps = steps + 1
