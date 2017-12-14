import sys
import collections

from timeit import default_timer as timer

start = timer()

layer_def = collections.defaultdict(int)

# parse input data
with open('inputs/day13_input.txt', 'r') as f:
    for line in f:
        row_data = line.split(':')
        layer_def[int(row_data[0].strip())] = int(row_data[1])

# layer_def[0] = 3
# layer_def[1] = 2
# layer_def[4] = 4
# layer_def[6] = 4

layers_count = max(layer_def.iterkeys()) + 1

def init_firewall():
    firewall = [-1 for elem in range(layers_count)]
    for layer in layer_def.iterkeys():
        firewall[layer] = 0;
    return firewall


def tick_firewall(f_wall):
    for layer in layer_def.iteritems():
        current_val = f_wall[layer[0]]
        max_val = (layer[1] - 1) * 2
        new_val = (current_val + 1) % max_val
        f_wall[layer[0]] = new_val

min_severity = 1500
delay = 0
prev_firewall_state = None

while min_severity > 0:
    if delay % 100000 == 0:
        print "delay: {}".format(delay)
    cached_firewall = prev_firewall_state or init_firewall()
    this_firewall = list(cached_firewall)

    tick_firewall(cached_firewall)
    prev_firewall_state = list(cached_firewall)

    # print this_firewall

    pos = 0
    severity = 0
    is_detected = False

    # print("delaying {}").format(delay)
    # for d in range(delay):
    #     tick_firewall(this_firewall)

    # print "running..."
    while pos < layers_count:
        if this_firewall[pos] == 0:
            is_detected = True
            sev = pos * layer_def[pos]
            severity += sev
            break
        tick_firewall(this_firewall)
        pos += 1

    # if severity < min_severity and
    if not is_detected:
        min_severity = 0
        print "min severity {} at delay {}".format(severity, delay)

    delay += 1

end = timer()
print "Elapsed Time: {}".format(end - start)