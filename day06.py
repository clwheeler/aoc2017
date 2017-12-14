initial_config = [4, 10, 4, 1, 8, 4, 9, 14, 5, 1, 14, 15, 0, 15, 3, 5]
# initial_config = [0, 2, 7, 0]


num_blocks = len(initial_config)
configurationHistory = []

def balanceMemory(input_banks):
    # find largest index
    mem_banks = input_banks
    maxValue = max(mem_banks)
    maxIndex = mem_banks.index(maxValue)
    mem_banks[maxIndex] = 0

    for x in range(1, maxValue + 1):
        updateInd = (maxIndex + x) % num_blocks
        mem_banks[updateInd] = mem_banks[updateInd] + 1

    return mem_banks

current_config = initial_config
numSteps = 0
stop = False

while not stop:
    if current_config in configurationHistory:
        print "Loop found on: {} on step: {}".format(current_config, numSteps)
        print "Loop size = {}".format(numSteps - configurationHistory.index(current_config))
        stop = True

    configurationHistory.append(list(current_config))
    current_config = balanceMemory(current_config)
    numSteps += 1
