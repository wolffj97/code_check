import sys


def unBurrow(letters):
    front = sorted(letters)
    vals = []
    counts = {"A": 0, "C": 0, "G": 0, "T": 0}
    for i in range(len(letters)):
        if letters[i] in counts.keys():
            temp = string[i] + str(counts[letters[i]])
            counts[letters[i]] += 1
            vals.append(temp)
        else:
            vals.append(letters[i])

    letters = vals
    vals = []
    counts = {"A": 0, "C": 0, "G": 0, "T": 0}
    for i in range(len(front)):
        if front[i] in counts.keys():
            temp = front[i] + str(counts[front[i]])
            counts[front[i]] += 1
            vals.append(temp)
        else:
            vals.append(front[i])
    front = vals

    current = letters.index('$')
    genesis = front[current][0]
    while len(genesis) < len(letters):
        current = letters.index(front[current])
        genesis += front[current][0]
    return genesis


if __name__ == '__main__':
    file = sys.argv[1]
    with open(file) as i:
        lines = i.read()
        lines = lines.split('\n')
    string = lines[0]

    print(unBurrow(string))


