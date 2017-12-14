import sys
from enum import Enum

class DIRS(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    NUM_DIRS = 3

def turnLeft(direction):
    if direction == DIRS.RIGHT:
        return DIRS.UP
    elif direction == DIRS.UP:
        return DIRS.LEFT
    elif direction == DIRS.LEFT:
        return DIRS.DOWN
    elif direction == DIRS.DOWN:
        return DIRS.RIGHT

def walk(fromPos, facing, length):
    if facing == DIRS.RIGHT:
        return (fromPos[0] + length, fromPos[1])
    elif facing == DIRS.UP:
        return (fromPos[0], fromPos[1] + length)
    elif facing == DIRS.LEFT:
        return (fromPos[0] - length, fromPos[1])
    elif facing == DIRS.DOWN:
        return (fromPos[0], fromPos[1] - length)
    else:
        print('bad direction')


elemList = [(0,0)]
aggValues = [1]

def genSpiralPosition(size):
    thisWalk = 0
    sideLength = 0
    expandLength = False
    walkDir = DIRS.RIGHT
    newPos = (0, 0)

    for x in range(0, size):
        newPos = walk(newPos, walkDir, 1)
        thisWalk += 1
        if thisWalk > sideLength:
            walkDir = turnLeft(walkDir)
            if expandLength:
                sideLength += 1
            expandLength = not expandLength
            thisWalk = 0
        elemList.append(newPos)

        thisAggValue = 0
        for b in range(0, x + 1):
            bPos = elemList[b]
            if abs(bPos[0] - newPos[0]) < 2 and abs(bPos[1] - newPos[1]) < 2:
                thisAggValue += aggValues[b]
        aggValues.append(thisAggValue)

        if thisAggValue > 265149:
            print "winner: {} = {}".format(x, thisAggValue)

    return newPos

pos = genSpiralPosition(int(sys.argv[1]) - 1)
# print elemList
print aggValues
print abs(pos[0]) + abs(pos[1])
