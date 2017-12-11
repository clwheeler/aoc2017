import sys
import collections
import codecs
hexlify = codecs.getencoder('hex')

twist_lengths = [130,126,1,11,140,2,255,207,18,254,246,164,29,104,0,224]
# twist_lengths = [3, 4, 1, 5]

input_string = []

for x in range(0, 256):
    input_string.append(x)

# print input_string

current_pos = 0
skip_size = 0

def do_hash(current_pos, skip_size, input_string):
    # print "starting at: {} with length {}".format(current_pos, length)
    substring = []
    # wrap list
    for ind in range(current_pos, current_pos + length):
        substring.append(input_string[ind % len(input_string)])
    # print "reversing: {}".format(substring)
    substring.reverse()
    for ind in range(current_pos, current_pos + length):
        input_string[ind % len(input_string)] = substring[ind - current_pos]
    current_pos += length
    current_pos += skip_size
    skip_size += 1
    current_pos = current_pos % len(input_string)
    return current_pos, skip_size, input_string

for length in twist_lengths:
    current_pos, skip_size, input_string = do_hash(current_pos, skip_size, input_string)

print "one time hash: {}".format(input_string)
print input_string[0] * input_string[1]

# part 2
twist_lengths = "130,126,1,11,140,2,255,207,18,254,246,164,29,104,0,224"
# twist_lengths = "1,2,3"
twist_lengths = [ord(char) for char in twist_lengths]
twist_lengths += [17, 31, 73, 47, 23]
num_rounds = 64

current_pos = 0
skip_size = 0
input_string = []
for x in range(0, 256):
    input_string.append(x)

print twist_lengths

for rnd in range(0, num_rounds):
    for length in twist_lengths:
        current_pos, skip_size, input_string = do_hash(current_pos, skip_size, input_string)

print "raw hash {}".format(input_string)

final_hash = []
for offset in range(0, 16):
    this_list = input_string[(offset * 16): (offset * 16)+16]
    this_val = reduce((lambda x, y: x ^ y), this_list)
    # print this_val
    final_hash.append(this_val)

print final_hash

hash_string = [hex(num) for num in final_hash]
hash_list = [string.replace('0x', '') for string in hash_string]
hash_list = ['0'+item for item in hash_list]
hash_list = [item[-2:] for item in hash_list]
print hash_list

print ''.join(hash_list)

