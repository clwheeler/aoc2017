
import sys
import collections

test_cases = [
                ["{}", 1],
                ["{{{}}}", 6],
                ["{{},{}}", 5],
                ["{{{},{},{{}}}}", 16],
                ["{<a>,<a>,<a>,<a>}", 1],
                ["{{<ab>},{<ab>},{<ab>},{<ab>}}", 9],
                ["{{<!!>},{<!!>},{<!!>},{<!!>}}", 9],
                ["{{<a!>},{<a!>},{<a!>},{<ab>}}", 3],
                ["{{<!>},{<!>},{<!>},{<a>}}", 3],
                ["{<!!> !!}", 1],
                ["{{<{<!> !> }>}}", 3],
                ["{<!> >}", 1],
                ["{<{ <}}>}", 3],
                ["{<{}}>}", 1],
]

# parse input data
with open('inputs/day9_input.txt', 'r') as f:
    for line in f:
        input_string = line

current_commands = []
open_nesting_chars = ['{', '<']
close_nesting_chars = ['}', '>']
escape_chars = ['!']

def process_char(char, score):
    # ignore escaped char
    if len(current_commands) > 0 and current_commands[-1] in escape_chars:
        # print "skipping: {}".format(char)
        current_commands.pop()
        return
    # process escape char
    if char in escape_chars and '<' in current_commands:

        current_commands.append(char)
        return

    # process other command chans
    if char in open_nesting_chars:
        current_commands.append(char)
        return

    if char in close_nesting_chars:
        # close > matches the first <
        if char == '>' and '<' in current_commands:
            # roll back to first < in the list
            # walk backwards to the first <?
            ind = current_commands.index('<')
            while len(current_commands) > ind:
                current_commands.pop()
            return
        elif char == '}' and '{' in current_commands:
            if current_commands[-1] == '{':
                score.append(current_commands.count('{'))
                current_commands.pop()
                return

for test in test_cases:
    score = []
    for char in test[0]:
        process_char(char, score)
    print "Expected {},  got: {} in {} groups".format(test[1], sum(score), len(score))

final_score = []
input_string = input_string.strip()
# print input_string
for char in input_string:
    process_char(char, final_score)

# print "file => {} in {} groups".format(sum(final_score), len(final_score))


# import sys
# import collections

# test_cases = [
#                 ["{}", 1],
#                 ["{{{}}}", 6],
#                 ["{{},{}}", 5],
#                 ["{{{},{},{{}}}}", 16],
#                 ["{<a>,<a>,<a>,<a>}", 1],
#                 ["{{<ab>},{<ab>},{<ab>},{<ab>}}", 9],
#                 ["{{<!!>},{<!!>},{<!!>},{<!!>}}", 9],
#                 ["{{<a!>},{<a!>},{<a!>},{<ab>}}", 3],
#                 ["{{<!>},{<!>},{<!>},{<a>}}", 3],
#                 ["{<!!> !!}", 1],
#                 ["{{<{<!> !> }>}}", 3],
#                 ["{<!> >}", 1],
#                 ["{<{ <}}>}", 3],
# ]

# # parse input data
# with open('inputs/day9_input.txt', 'r') as f:
#     for line in f:
#         input_string = line

# escape_chars = ['!']

# ignore_next = False
# is_garbage = False
# level = 0

#     # # process other command chans
#     # if char in open_nesting_chars:
#     #     current_commands.append(char)
#     #     return

#     # if char in close_nesting_chars:
#     #     # close > matches the first <
#     #     if char == '>' and '<' in current_commands:
#     #         # roll back to first < in the list
#     #         # walk backwards to the first <?
#     #         ind = current_commands.index('<')
#     #         while len(current_commands) > ind:
#     #             current_commands.pop()
#     #         return
#     #     elif char == '}' and '{' in current_commands:
#     #         if current_commands[-1] == '{':
#     #             score.append(current_commands.count('{'))
#     #             current_commands.pop()
#     #             return


# # final_score = []
# # input_string = input_string.strip()
# # print input_string

# for test in test_cases:
#     score = []
#     level = 0
#     for char in test[0]:
#         if is_garbage:
#             if ignore_next:
#                 ignore_next = False
#             elif char == '!':
#                 ignore_next = True
#             elif char == '>':
#                 is_garbage = False

#         elif char == '<':
#             is_garbage = True

#         elif char == '{':
#             level += 1

#         elif char == '}':
#             score.append(level)
#             level = level - 1

#     print "Expected {},  got: {} in {} groups".format(test[1], sum(score), (score))


# score = []
# level = 0
# garbage_chars = 0

# for char in input_string:
#     if is_garbage:
#         if ignore_next:
#             ignore_next = False
#         elif char == '!':
#             ignore_next = True
#         elif char == '>':
#             is_garbage = False
#         else:
#             garbage_chars += 1

#     elif char == '<':
#         is_garbage = True

#     elif char == '{':
#         level += 1

#     elif char == '}':
#         score.append(level)
#         level = level - 1

# print "Expected {},  got: {} in {} groups".format(0, sum(score), len(score))
# print garbage_chars