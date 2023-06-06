import sys


def suffixes(pattern):
    spots = []
    matches = {}
    for i in range(len(pattern)):
        spots.append(pattern[i:])
        matches[pattern[i:]] = i
    fixed = []
    spots = sorted(spots)
    for item in spots:
        fixed.append(str(matches[item]))
    return fixed


if __name__ == "__main__":

    filename = sys.argv[1]
    f = open(filename, "r")
    lines = f.readlines()
    base = []
    for line in lines:
        line = line.strip().split(' ')
        for item in line:
            base.append(item)
    index = suffixes(base[0])

    print(" ".join(index))
