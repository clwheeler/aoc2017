import sys
import re
import collections
import operator

from timeit import default_timer as timer

test_input = """p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
"""


def parse_input_data(input_data=None):
    data = []
    re_pattern = r"p=<([\-0-9]+),([\-0-9]+),([\-0-9]+)>, v=<([\-0-9]+),([\-0-9]+),([\-0-9]+)>, a=<([\-0-9]+),([\-0-9]+),([\-0-9]+)>"

    with open('inputs/day20_input.txt', 'r') as f:
        for line in f:
            regex = re.match(re_pattern, line)
            pos = (int(regex.group(1)), int(regex.group(2)), int(regex.group(3)))
            vel = (int(regex.group(4)), int(regex.group(5)), int(regex.group(6)))
            acc = (int(regex.group(7)), int(regex.group(8)), int(regex.group(9)))
            data.append([pos, vel, acc])

    # for line in test_input.splitlines():
    #     regex = re.match(re_pattern, line)
    #     pos = (int(regex.group(1)), int(regex.group(2)), int(regex.group(3)))
    #     vel = (int(regex.group(4)), int(regex.group(5)), int(regex.group(6)))
    #     acc = (int(regex.group(7)), int(regex.group(8)), int(regex.group(9)))
    #     data.append([pos, vel, acc])

    return data


def tuple_add(a, b):
    # print ("{} + {} = {}").format(a, b, tuple(map(operator.add, a, b)))
    return tuple(map(operator.add, a, b))

class particle(object):

    def __init__(self, pos, vel, acc, ind):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.index = ind
        self.state = "ACTIVE"

    def tick(self):
        self.vel = tuple_add(self.vel, self.acc)
        self.pos = tuple_add(self.pos, self.vel)

    def get_distance_to(self, point):
        return abs(self.pos[0] - point[0]) + abs(self.pos[1] - point[1]) + abs(self.pos[2]  - point[2])

    def get_index(self):
        return self.index

    def destroy(self):
        self.state = "DESTROYED"


# start = timer()

all_particles = []

particles_def = parse_input_data()

ind = 0
for part in particles_def:
    this_particle = particle(part[0], part[1], part[2], ind)
    all_particles.append(this_particle)
    ind += 1

min_distance_list = []

for step in range(100):
    min_distance = sys.maxint
    min_distance_index = 0

    for index in range(len(all_particles)):
        for inner_ind in range(index+1, len(all_particles)):
            if all_particles[index].pos == all_particles[inner_ind].pos:
                all_particles[index].destroy()
                all_particles[inner_ind].destroy()

    # don't want to deal with index issues on remove()
    new_list = []
    for particle in all_particles:
        if particle.state != "DESTROYED":
            new_list.append(particle)
    all_particles = list(new_list)

    for particle in all_particles:
        this_dist = particle.get_distance_to((0, 0, 0))
        if this_dist < min_distance:
            min_distance_index = particle.get_index()
            min_distance = this_dist

    min_distance_list.append(min_distance_index)

    for particle in all_particles:
        particle.tick()

    print len(all_particles)

print min_distance_list

# end = timer()
# print "Elapsed Time: {}".format(end - start)
