match_count = 0
with open('aocd4_input.txt', 'r') as f:
    for line in f:
        words = line.replace('\n', '').split(' ')
        print [''.join(sorted([letter for letter in word])) for word in words]
        word_set = set([''.join(sorted([letter for letter in word])) for word in words])
        if len(word_set) == len(words):
            match_count += 1
print match_count
