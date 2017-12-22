import sys
import collections
import codecs


def do_spinlock(inc_steps, total_steps):
    total_steps += 1
    buffer_state = collections.deque()
    # current_position = 0

    for x in range(0, total_steps):
        if x % 100000 == 0:
            print x

        if not buffer_state:
            buffer_state.append(0)
            continue
        for i in range(inc_steps % len(buffer_state)):
            buffer_state.append(buffer_state.popleft())

        buffer_state.append(x)
        # new_pos = (current_position + inc_steps) % len(buffer_state)
        # if new_pos == len(buffer_state) - 1:
        #     buffer_state.append(x)
        # else:
        #     buffer_state.insert(((new_pos + 1) % len(buffer_state)), x)
        # current_position = (new_pos + 1) % len(buffer_state)
        # print buffer_state

    # print "{}: {}".format(current_position, buffer_state)
    print "{}, {}".format(buffer_state[-1], buffer_state[0])
    zero_pos = list(buffer_state).index(0)
    print "0 at: {}, {}, {}".format(buffer_state[zero_pos - 1], buffer_state[zero_pos], buffer_state[zero_pos + 1])

do_spinlock(3, 2017)

do_spinlock(335, 2017)

do_spinlock(335, 50000000)
