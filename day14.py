import sys
import collections
import codecs

def do_hash(current_pos, skip_size, input_string, length):
    # print "starting at: {} with length {}".format(current_pos, length)
    substring = []
    # wrap list
    for ind in range(current_pos, current_pos + length):
        substring.append(input_string[ind % len(input_string)])
    substring.reverse()

    for ind in range(current_pos, current_pos + length):
        input_string[ind % len(input_string)] = substring[ind - current_pos]
    current_pos += length
    current_pos += skip_size
    skip_size += 1
    current_pos = current_pos % len(input_string)
    return current_pos, skip_size, input_string


def get_full_knot_hash(twist_input):
    twist_lengths = twist_input
    twist_lengths = [ord(char) for char in twist_lengths]
    twist_lengths += [17, 31, 73, 47, 23]
    num_rounds = 64

    current_pos = 0
    skip_size = 0
    input_string = []
    for x in range(0, 256):
        input_string.append(x)

    for rnd in range(0, num_rounds):
        for length in twist_lengths:
            current_pos, skip_size, input_string = do_hash(current_pos, skip_size, input_string, length)

    final_hash = []
    for offset in range(0, 16):
        this_list = input_string[(offset * 16): (offset * 16)+16]
        this_val = reduce((lambda x, y: x ^ y), this_list)
        # print this_val
        final_hash.append(this_val)

    hash_string = [hex(num) for num in final_hash]
    hash_list = [string.replace('0x', '') for string in hash_string]
    hash_list = ['0'+item for item in hash_list]
    hash_list = [item[-2:] for item in hash_list]

    return ''.join(hash_list)

input_key = 'hwlqcszp-'
used_blocks = 0
disk_map = []

for disk_row in range(128):
    row_str = str(disk_row)
    row_key = input_key + row_str

    this_hash = get_full_knot_hash(row_key)
    binary_hash = bin(int(this_hash, 16))[2:]
    binary_hash = '0000000000000000000000000000000000000000000000000000000000000' + binary_hash
    binary_hash = binary_hash[-128:]
    used_blocks += binary_hash.count('1')
    disk_map.append([char for char in binary_hash])

print "{} blocks used".format(used_blocks)

# print disk_map
groups = []

class BLOCK_STATUS(object):
    EMPTY = '0'
    USED = '1'
    SEEN = '3'

def find_contiguous_blocks_dfs(my_disk_map):

    def check_index(x, y, group_id):
        if x not in range(0, 128) or y not in range(0, 128):
            return 0

        this_value = my_disk_map[x][y]
        if this_value == '1':
            my_disk_map[x][y] = group_id
            # BLOCK_STATUS.SEEN
            # check neighbors
            group_size = 1
            group_size += check_index(x-1, y, group_id)
            group_size += check_index(x+1, y, group_id)
            group_size += check_index(x, y-1, group_id)
            group_size += check_index(x, y+1, group_id)
            return group_size

        else:
            return 0

    for row_ind in range(128):
        for col_ind in range(128):
            group_size = check_index(row_ind, col_ind, row_ind * col_ind)
            if group_size > 0:
                groups.append(group_size)

find_contiguous_blocks_dfs(disk_map)


print len(groups)
