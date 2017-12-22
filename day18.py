import sys
import re
import collections

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
        with open('inputs/day18_input.txt', 'r') as f:
            for line in f:
                data.append(line.strip().split(' '))
    else:
        for line in input_data.splitlines():
            data.append(line.strip().split(' '))

    print data
    return data


COMMAND = 0
TARGET = 1
VALUE = 2

class DUET_RUNNER(object):
    current_pos = 0
    registers = collections.defaultdict(int)
    inst_list = []

    def __init__(self, instructions):
        self.inst_list = instructions

    def get_register_value(self, name):
        try:
            val = int(name)
            return val
        except ValueError:
            pass
        return self.registers[name]

    def set_register(self, name, value):
        self.registers[name] = int(value)

    def execute_command(self, instruction):
        if instruction[COMMAND] == 'snd':
            self.last_tone = self.get_register_value(instruction[TARGET])
            print "Playing {}".format(self.last_tone)
        elif instruction[COMMAND] == 'set':
            self.set_register(instruction[TARGET], self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'add':
            old_val = self.get_register_value(instruction[TARGET])
            self.set_register(instruction[TARGET], old_val + self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'mul':
            old_val = self.get_register_value(instruction[TARGET])
            self.set_register(instruction[TARGET], old_val * self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'mod':
            old_val = self.get_register_value(instruction[TARGET])
            self.set_register(instruction[TARGET], old_val % self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'rcv':
            this_val = self.get_register_value(instruction[TARGET])
            if this_val:
                print "Recovering {}".format(self.last_tone)
                raise ValueError()
        elif instruction[COMMAND] == 'jgz':
            this_val = self.get_register_value(instruction[TARGET])
            if this_val > 0:
                self.current_pos += int(instruction[VALUE])
                return 0
        return 1

    def run(self):
        OUT_OF_BOUNDS = False
        count = 0
        while not OUT_OF_BOUNDS:
            if self.current_pos < 0 or self.current_pos > len(self.inst_list):
                OUT_OF_BOUNDS = True
            inc = self.execute_command(self.inst_list[self.current_pos])

            self.current_pos += inc
            count += 1


# start = timer()

# DUET_RUNNER(parse_input_data(None)).run()

# end = timer()
# print "Elapsed Time: {}".format(end - start)

class DUET_RUNNER_PART_2(object):

    def __init__(self, instructions, program_id):
        self.message_queue = collections.deque()
        self.current_pos = 0
        self.registers = collections.defaultdict(int)

        self.inst_list = instructions
        self.registers['p'] = program_id


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
        if instruction[COMMAND] == 'snd':
            return self.get_register_value(instruction[TARGET])
        elif instruction[COMMAND] == 'set':
            self.set_register(instruction[TARGET], self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'add':
            old_val = self.get_register_value(instruction[TARGET])
            self.set_register(instruction[TARGET], old_val + self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'mul':
            old_val = self.get_register_value(instruction[TARGET])
            self.set_register(instruction[TARGET], old_val * self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'mod':
            old_val = self.get_register_value(instruction[TARGET])
            self.set_register(instruction[TARGET], old_val % self.get_register_value(instruction[VALUE]))
        elif instruction[COMMAND] == 'rcv':
            if len(self.message_queue) == 0:
                return 'wait'
            else:
                write_val = self.message_queue.popleft()
                self.set_register(instruction[TARGET], write_val)
        elif instruction[COMMAND] == 'jgz':
            this_val = self.get_register_value(instruction[TARGET])
            if this_val > 0:
                self.current_pos += self.get_register_value(instruction[VALUE])
                return 'jmp'
        return 'inc'

    # def run(self):
    #     OUT_OF_BOUNDS = False
    #     count = 0
    #     while not OUT_OF_BOUNDS:
    #         if self.current_pos < 0 or self.current_pos > len(self.inst_list):
    #             OUT_OF_BOUNDS = True
    #         inc = self.execute_command(self.inst_list[self.current_pos])

    #         if inc == 'inc':
    #             self.current_pos += inc
    #         count += 1

HALT = False

runner_1 = DUET_RUNNER_PART_2(parse_input_data(None), 1)
runner_0 = DUET_RUNNER_PART_2(parse_input_data(None), 0)

send_val = 0

while not HALT:
    if runner_0.current_pos < 0 or runner_0.current_pos > len(runner_0.inst_list):
        print 'runner 0 OOB'
        HALT = True
    if runner_1.current_pos < 0 or runner_1.current_pos > len(runner_1.inst_list):
        print 'runner 1 OOB'
        HALT = True

    val_0 = runner_0.execute_command()
    val_1 = runner_1.execute_command()

    if val_0 == 'inc':
        runner_0.current_pos += 1
    if val_1 == 'inc':
        runner_1.current_pos += 1

    if val_0 == 'wait' and val_1 == 'wait':
        print 'deadlock'
        HALT = True

    if type(val_0) is int:
        runner_1.send_message(val_0)
        runner_0.current_pos += 1
    if type(val_1) is int:
        runner_0.send_message(val_1)
        send_val += 1
        print send_val
        runner_1.current_pos += 1
