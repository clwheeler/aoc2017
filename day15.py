import sys
import collections
import codecs

def gen_next_value(factor, this_value, qualifier):
    result = factor * this_value
    result = result % 2147483647

    while result % qualifier != 0:
        result = factor * result
        result = result % 2147483647

    return result

class day15(object):
    # prev_value_A = 65
    # prev_value_B = 8921

    prev_value_A = 591
    prev_value_B = 393

    factor_A = 16807
    factor_B = 48271

    matches = []

    # def part1(self):
    #     for x in range(0, 40000000):
    #         if x % 1000000 == 0:
    #             print x

    #         value_A = gen_next_value(factor_A, prev_value_A, 1)
    #         value_B = gen_next_value(factor_B, prev_value_B, 1)

    #         binary_A = bin(int(value_A))[-16:]
    #         binary_B = bin(int(value_B))[-16:]

    #         if binary_A == binary_B:
    #             matches.append(x)

    #         prev_value_A = value_A
    #         prev_value_B = value_B

    #     print len(matches)

    def part2(self):
        for x in range(0, 5000000):
            if x % 1000000 == 0:
                print x
            value_A = gen_next_value(self.factor_A, self.prev_value_A, 4)
            value_B = gen_next_value(self.factor_B, self.prev_value_B, 8)

            if (value_A & 0xffff) == (value_B & 0xffff):
                self.matches.append(x)

            self.prev_value_A = value_A
            self.prev_value_B = value_B

            # print "{}: {}, {}".format(x, value_A, value_B)

        print len(self.matches)


day15().part2()
