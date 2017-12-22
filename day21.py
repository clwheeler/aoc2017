import sys
import re
import collections
import operator
import math

from timeit import default_timer as timer

test_input = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"""

# Store transforms as strings
def parse_input_data(input_data=None):
    data = dict()
    # re_pattern = r"p=<([\-0-9]+),([\-0-9]+),([\-0-9]+)>, v=<([\-0-9]+),([\-0-9]+),([\-0-9]+)>, a=<([\-0-9]+),([\-0-9]+),([\-0-9]+)>"

    if input_data:
        for line in test_input.splitlines():
            line_parts = line.strip().split(" => ")
            src = line_parts[0]
            res = line_parts[1]
            data[src] = res
        return data

    with open('inputs/day21_input.txt', 'r') as f:
        for line in f:
            line_parts = line.strip().split(" => ")
            src = line_parts[0]
            res = line_parts[1]
            data[src] = res

    return data

class ROTS(object):

    @staticmethod
    def NONE(x):
        return x

    @staticmethod
    def ROT_90(x):
        manip = x.split('/')
        manip_list = [[char for char in row] for row in manip]
        rotated = zip(*manip_list[::-1])
        rotated = [''.join(row) for row in rotated]
        return '/'.join(rotated)

    @staticmethod
    def ROT_180(x):
        return ROTS.ROT_90(ROTS.ROT_90(x))

    @staticmethod
    def ROT_270(x):
        return ROTS.ROT_90(ROTS.ROT_90(ROTS.ROT_90(x)))

ALL_ROTS = [ROTS.NONE, ROTS.ROT_90, ROTS.ROT_180, ROTS.ROT_270]


class FLIPS(object):
    @staticmethod
    def NONE(x):
        return x

    @staticmethod
    def VERT(x):
        manip = x.split('/')
        manip.reverse()
        return '/'.join(manip)

    @staticmethod
    def HORIZ(x):
        manip = x.split('/')
        for row in range(len(manip)):
            string = manip[row]
            manip[row] = string[::-1]
        return '/'.join(manip)

    @staticmethod
    def BOTH(x):
        return FLIPS.VERT(FLIPS.HORIZ(x))

ALL_FLIPS = [FLIPS.NONE, FLIPS.VERT, FLIPS.HORIZ, FLIPS.BOTH]


def transform_panel(panel, transforms):
    # lookup panel

    for manip in ALL_FLIPS:
        manip_panel = manip(panel)
        # if manip_panel in transforms:
        #     return transforms[manip_panel]

        for manip_2 in ALL_ROTS:
            manip_panel = manip_2(manip(panel))
            if manip_panel in transforms:
                return transforms[manip_panel]

    raise ValueError('Missing transform')


def convert_to_panels(panel_size, pic_string):
    rows = pic_string.split('/')

    panel_row = len(rows) / panel_size
    num_panels = panel_row ** 2
    panels = ['' for x in range(num_panels)]

    # for row in rows:
    #     print "".join(row)

    # split into 3x3 blocks
    for r_ind, row in enumerate(rows):
        panel_y = r_ind / panel_size
        for char_ind, char in enumerate(row.strip()):
            panel_x = char_ind / panel_size
            list_index = (panel_y * panel_row) + panel_x
            # print "{}, {} = index {}".format(panel_x, panel_y, list_index)
            panels[list_index] = panels[list_index] + char

    # insert line breaks
    new_panels = []
    for panel in panels:
        new_panel = '/'.join(panel[i:i+panel_size] for i in range(0, len(panel), panel_size))
        new_panels.append(new_panel)

    return new_panels


def convert_to_picture(new_panels):
    num_rows_in_panel = len(new_panels[0].split('/'))
    prev_panel_width = int(math.sqrt(len(new_panels)))
    num_dest_rows = num_rows_in_panel * prev_panel_width

    picture_rows = ['' for x in range(num_dest_rows)]

    # print picture_rows

    for row_ind, panel in enumerate(new_panels):
        this_panel = panel.split('/')

        # print "this panel: {}".format(this_panel)

        for ind, chunk in enumerate(this_panel):
            index_to_update = ((row_ind / prev_panel_width) * num_rows_in_panel) + ind
            # print "row_ind: {}, ind: {} = {}".format(row_ind, ind, index_to_update)
            old_val = picture_rows[index_to_update]
            new_val = old_val + chunk
            picture_rows[index_to_update] = new_val

    return '/'.join(picture_rows)
# start = timer()

# setup
transforms = parse_input_data()
initial_state = ".#./..#/###"
# initial_state = "#..#/..../..../#..#"

picture_state = initial_state

for iterations in range(18):
    panels = []
    rows = picture_state.split('/')

    if len(rows) % 2 == 0:
        panels = convert_to_panels(2, picture_state)
    else:
        panels = convert_to_panels(3, picture_state)

    # for ind, this_panel in enumerate(panels):
    #     print "Panel {}: {}".format(ind, "".join(this_panel))

    print '================='
    for x in picture_state.split('/'):
        print x

    new_panels = []
    for panel in panels:
        new_panels.append(transform_panel(panel, transforms))

    # print new_panels
    picture_state = convert_to_picture(new_panels)

    print picture_state.count('#')
# end = timer()
# print "Elapsed Time: {}".format(end - start)
