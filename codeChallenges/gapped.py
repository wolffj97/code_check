import sys


def createFrags(k, d, kmers):

    genesis = 0

    for x in range(len(kmers)):
        p = kmers[x][:k-1] + kmers[x][k+1:-1]
        check = False
        for y in range(len(kmers)):
            s = kmers[y][1:k] + kmers[y][k+2:]
            if p == s:
                check = True
        if not check:
            genesis = x

    indices = [genesis]

    i = genesis
    while True:
        suffix = kmers[i][1:k] + kmers[i][k+2:]
        added = False

        for j in range(len(kmers)):
            prefix = kmers[j][:k-1] + kmers[j][k+1:-1]

            if suffix == prefix:
                indices.append(j)
                i = j
        if len(indices) == len(kmers):
            break

    # print(indices)
    output = kmers[indices[0]][:k]

    for j in range(len(indices)):
        if j == 0:
            continue
        output += kmers[indices[j]][k-1]

    num = len(indices) - (k+d)
    # print(num)
    while num < len(indices):
        output += kmers[indices[num]][-1]
        num += 1

    return output


if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename, "r")
    lines = f.readlines()
    for index in range(len(lines)):
        lines[index] = lines[index].strip()

    k = int(sys.argv[2])
    d = int(sys.argv[3])

    val = createFrags(k, d, lines)

    print(val)
