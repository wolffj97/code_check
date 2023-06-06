import sys


def counter(string):
    counts = {"A": 0, "C": 0, "G": 0, "T": 0}
    fixed = []
    for letter in string:
        if letter in counts.keys():
            temp = letter + str(counts[letter])
            fixed.append(temp)
            counts[letter] += 1
        else:
            fixed.append(letter)
    return fixed


def lastToFirst(last, first):
    index = []
    for i in range(len(last)):
        index.append(first.index(last[i]))

    return index


def matcher(string, pattern, firsts, counts):
    string = list(string)
    top = 0
    bottom = len(string) - 1
    alphabet = ["A", "C", "G", "T"]
    while top <= bottom:
        if pattern != "":
            char = pattern[-1]
            symbol = alphabet.index(pattern[-1])
            pattern = pattern[0:-1]

            if char in string[top:bottom+1]:
                shift = firsts[symbol]
                top = shift + string[0:top].count(char)
                bottom = shift + string[0:bottom+1].count(char) - 1
            else:
                return '0'

        else:
            return str(bottom - top + 1)
    return '0'


if __name__ == "__main__":

    filename = sys.argv[1]
    f = open(filename, "r")
    lines = f.read()
    lines = lines.split('\n')
    string = lines[0]
    patterns = lines[1].split(' ')

    front = sorted(string)
    counts = {"$": 1,
              "A": string.count("A"),
              "C": string.count("C"),
              "G": string.count("G"),
              "T": string.count("T")}
    firsts = [front.index("A"),
              front.index("C"),
              front.index("G"),
              front.index("T")]

    nums = []
    for pattern in patterns:
        nums.append(matcher(string, pattern, firsts, counts))

    print(" ".join(nums))

