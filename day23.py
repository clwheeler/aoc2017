import sys
import re
import collections
import math

from timeit import default_timer as timer

test_input = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
"""


def parse_input_data(input_data):
    data = []

    if not input_data:
        with open('inputs/day23_input.txt', 'r') as f:
            for line in f:
                data.append(line.strip().split(' '))
    else:
        for line in input_data.splitlines():
            data.append(line.strip().split(' '))

    return data


COMMAND = 0
TARGET = 1
VALUE = 2

# start = timer()

# end = timer()
# print "Elapsed Time: {}".format(end - start)

class COPROCESSER(object):

    mult_ct = 0

    def __init__(self, instructions, program_id):
        self.message_queue = collections.deque()
        self.current_pos = 0
        self.registers = collections.defaultdict(int)

        self.inst_list = instructions
        # self.registers['a'] = 0


    def send_message(self, val):
        self.message_queue.append(val)

    def get_register_value(self, name):
        try:
            val = int(name)
            return val
        except ValueError:
            pass
        return self.registers[name]

    def set_register(self, name, value):
        self.registers[name] = int(value)

    def execute_command(self):
        instruction = self.inst_list[self.current_pos]
        # print instruction
        if instruction[COMMAND] == 'set':
            self.set_register(instruction[TARGET], self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'sub':
            old_val = self.get_register_value(instruction[TARGET])
            self.set_register(instruction[TARGET], old_val - self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'mul':
            COPROCESSER.mult_ct += 1
            print COPROCESSER.mult_ct

            old_val = self.get_register_value(instruction[TARGET])
            self.set_register(instruction[TARGET], old_val * self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'jnz':
            this_val = self.get_register_value(instruction[TARGET])
            if this_val != 0:
                self.current_pos += self.get_register_value(instruction[VALUE])
                return 'jmp'

        return 'inc'

    def get_register_display(self):
        keys = [key for key in self.registers.keys()]
        sort_keys = sorted(keys)
        keys = []
        for key in sort_keys:
            keys.append(self.registers[key])
        return keys

HALT = True

runner_0 = COPROCESSER(parse_input_data(None), 0)

while not HALT:
    if runner_0.current_pos < 0 or runner_0.current_pos >= len(runner_0.inst_list):
        print 'runner 0 OOB'
        print '{}'.format(runner_0.get_register_display())
        HALT = True
        break

    val_0 = runner_0.execute_command()
    # print 'after line: {}, {}'.format(runner_0.current_pos + 1, runner_0.get_register_display())

    # if tick_ct > 100000:
    #     print 'after line: {}, {}'.format(runner_0.current_pos + 1, runner_0.get_register_display())

    if val_0 == 'inc':
        runner_0.current_pos += 1


def simulate_processor():
    mult_ct = 0
    # 0 == Debug
    a = 1
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = 0

    b = 67
    c = b

    if a != 0:
        b = b * 100
        mult_ct += 1
        b = b + 100000
        c = b
        c = c + 17000
    else:
        print "DEBUG"

    run_main = True

    while run_main:
        f = 1
        d = 2
        run_outer = True
        while run_outer:
            e = 2
            run_inner = True
            while run_inner:
                if d * e == b:
                    f = 0
                if d * e > b:
                    run_inner = False
                e = e + 1
                if e == b:
                    run_inner = False
            d = d + 1
            if d > int(math.sqrt(b)):
                run_outer = False

        if f == 0:
            h = h + 1

        # print "{} / {}".format(b, c)

        if b == c:
            run_main = False
        else:
            b = b + 17

    # print "mult_ct: {}".format(mult_ct)
    print "[{}, {}, {}, {}, {}, {}, {}, {}]".format(a, b, c, d, e, f, g, h)

simulate_processor()
