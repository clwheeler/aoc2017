import sys
import collections

DiscData = collections.namedtuple('DiscData', ('weight', 'children'))
allDiscData = dict()
all_discs = []

# parse input data
with open('inputs/day7_input.txt', 'r') as f:
    for line in f:
        row = line.split('->')
        children = []
        if len(row) > 1:
            children = [elem.strip() for elem in row[1].split(',')]
        discInfo = row[0].split(' ')
        allDiscData[discInfo[0]] = DiscData(int(discInfo[1].strip('()\n')), children)
        all_discs.append(discInfo[0])

def findParentNode(name):
    for elem in all_discs:
        discData = allDiscData[elem]
        if name in discData.children:
            return findParentNode(elem)
    print "no parent, {} is the root".format(name)
    return None

for elem in all_discs:
    discData = allDiscData[elem]
    if len(discData.children) == 0:
        findParentNode(elem)
        break

root_node = 'veboyvy'

# from root
# get weight of all children
# if all are the same, try again on the children
# if one is different:
# only try on this branch
# print this branch

def detect_imbalance(name):
    discData = allDiscData[name]
    c_weights = dict()
    weight_sum = 0
    imbalance_found = False

    # get children weights
    for child in discData.children:
        this_weight = detect_imbalance(child)
        weight_sum += this_weight
        c_weights[child] = this_weight

    # detect children imbalance
    for each_weight in c_weights.iteritems():
        if each_weight[1] != weight_sum / len(c_weights):
            imbalance_found = True

    if imbalance_found:
        print "{} is imbalanced: ".format(name)
        for each_weight in c_weights.iteritems():
            print "   {}: {} != {}".format(each_weight[0], each_weight[1], weight_sum / len(c_weights))

    return discData.weight + weight_sum

detect_imbalance(root_node)

outputs = []
def print_from(name, level=0):
    discData = allDiscData[name]
    weight = discData.weight

    # get children weights
    for childName in discData.children:
        childData = allDiscData[childName]
        weight += print_from(childName, level+1)

    outStr = ''
    for x in range(0, level):
        outStr += ' '
    outputs.append("{}{} weighs {}".format(outStr, name, weight))
    return weight

print_from('obxrn')
for op in reversed(outputs):
    print op