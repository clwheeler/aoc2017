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
        self.registers['a'] = 1
        # self.registers['d'] = 100000
        # [1, 106700, 123700, 2, 40303, 1, 2, 0]
        self.registers['a'] = 1
        self.registers['b'] = 106700
        self.registers['c'] = 123700
        self.registers['d'] = 2
        self.registers['e'] = 40303
        self.registers['f'] = 1
        self.registers['g'] = 2
        self.registers['h'] = 0
        self.current_pos = 11


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
            # if instruction[TARGET] == 'd' and self.get_register_value(instruction[VALUE]) < 100000:
            #     # print 'd'
            #     # self.set_register('d', 100000)
            # else:
            self.set_register(instruction[TARGET], self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'sub':
            old_val = self.get_register_value(instruction[TARGET])
            self.set_register(instruction[TARGET], old_val - self.get_register_value(instruction[VALUE]))
            # if instruction[TARGET] == 'e' and instruction[VALUE] == -1:
            #     if old_val < 106700:
            #         print "skip e"
            #         self.set_register(instruction[TARGET], 106700)

        elif instruction[COMMAND] == 'mul':
            # COPROCESSER.mult_ct += 1
            # print COPROCESSER.mult_ct
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

tick_ct = 0
last_h_value = 0


# while not HALT:
while tick_ct < 40:
    tick_ct += 1

    if runner_0.current_pos < 0 or runner_0.current_pos >= len(runner_0.inst_list):
        print 'runner 0 OOB'
        HALT = True
        break

    val_0 = runner_0.execute_command()
    print 'after line: {}, {}'.format(runner_0.current_pos + 1, runner_0.get_register_display())

    # if tick_ct > 100000:
    #     print 'after line: {}, {}'.format(runner_0.current_pos + 1, runner_0.get_register_display())

    if val_0 == 'inc':
        runner_0.current_pos += 1

    if runner_0.registers['h'] != last_h_value:
        last_h_value = runner_0.registers['h']
        print last_h_value

    # if tick_ct % 100000 == 0:
        # runner_0.print_registers()
            # registers = runner_0.itervalues()
        # print "{} ticks, h = {}".format(tick_ct, runner_0.registers['h'])
    # if val_1 == 'inc':
    #     runner_1.current_pos += 1

    # if val_0 == 'wait' and val_1 == 'wait':
    #     print 'deadlock'
    #     HALT = True

    # if type(val_0) is int:
    #     runner_1.send_message(val_0)
    #     runner_0.current_pos += 1
    # if type(val_1) is int:
    #     runner_0.send_message(val_1)
    #     send_val += 1
    #     print send_val
    #     runner_1.current_pos += 1

print runner_0.registers['h']

a = 1
b = 106700
c = 123700
d = 2
e = 40303
f = 1
g = 2
h = 0

def simulate_processor():
    a, b, c, d, e, f, g, h = 0

    a = 1
    b = 106700
    c = 123700
    d = 2
    e = 2
    f = 1

    g = 0

    # 12
    while True:
        while g == 0:
            while g == 0:
                g = (d * e) - b
                if g == 0:
                    f = 0
                e = e + 1
                g = e - b
            d = d + 1
            g = d - b

        if f == 0:
            h = h + 1

        g = b - 123700

        if g == 0:
            print "h = {}".format(h)
            raise Exception("Halt OOB")

        b = b + 17

simulate_processor()

a = 1
b = 106700
c = 123700
d = 2
e = 40303
f = 1
g = 2
h = 0

def simulate_processor_opt():
    # after line: 12, [1, 106700, 123700, 2, 40303, 1, 2, 0]

    global a, b, c, d, e, f, g, h
    loop_ct = 0
    found = False

    while True:
        print "b: {}, h = {}".format(b, h)
        for x in range(2, b):
            # print "x: {}".format(x)
            for y in range(2, b / x):
                # print "y: {}".format(y)
                loop_ct += 1
                if (x * y) == b:
                    f = 0
                # print "opt inner: [{}, {}, {}, {}, {}, {}, {}, {}]".format(a, b, c, d, e, f, g, h)
                # if loop_ct == 4:
                #     return
            # print "opt outer: [{}, {}, {}, {}, {}, {}, {}, {}]".format(a, b, c, d, e, f, g, h)
        if f == 0:
            h = h + 1

        if b == 123700:
            print h
            raise ValueError('Halt')

        b = b + 17

# simulate_processor_opt()

def find_factors():
    factor_found = False
    b = 106700
    h = 0

    while b < 123700:
        root = int(math.sqrt(b)) + 1
        print b
        for x in range(2, root):
            for y in range(2, root):
                if x * y == b:
                    factor_found = True

        if factor_found:
            h += 1

        b += 17

    print h

find_factors()
