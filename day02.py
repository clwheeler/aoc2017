import sys

def getRowValue(row):
    for first_ind in range(0, len(word_nums)):
        for other_ind in range(first_ind, len(word_nums)):
            first_val = word_nums[first_ind]
            other_val = word_nums[other_ind]
            if first_val > other_val and first_val % other_val == 0:
                return first_val / other_val
    print 'failure: {}'.format(row)

checksum = 0
with open(sys.argv[1], 'r') as f:
    for line in f:
        words = line.replace('\n', '').split('\t')
        word_nums = [int(word) for word in words]
        word_nums = sorted(word_nums, reverse=True)
        checksum += getRowValue(word_nums)
print checksum
