import sys


# distances is a dictionary of nodes, connecting to
def neighborJoin(distances, nodes):
    n = nodes
    tree = {}

    if len(distances) == 2:
        alpha = 0
        for key in distances.keys():
            for other in distances[key].keys():
                if distances[key][other] == 0:
                    continue
                tree[key] = [other, distances[key][other]]
                return tree

    stars, total = dStar(distances)
    i, j = selector(stars)

    # these steps are for finding limb length for found neighbors
    delta = total[i] - total[j]
    delta = delta / (len(distances) - 2)

    limbI = (distances[i][j] + delta) / 2
    limbJ = (distances[i][j] - delta) / 2
    parent = n
    n += 1

    # these are for making the new distance matrix
    # add a new row/column m to D so that Dk,m = Dm,k = (1/2)(Dk,i + Dk,j - Di,j) for any k
    follow = {}
    for key in distances.keys():
        if key == i or key == j:
            continue
        row = distances[key]
        follow[key] = {}
        for index in row.keys():
            if index == i or index == j:
                continue
            follow[key][index] = row[index]
    dad = {parent: 0}
    for key in follow.keys():
        newVal = 0.5 * (distances[i][key] + distances[j][key] - distances[i][j])
        follow[key][parent] = newVal
        dad[key] = newVal
    follow[parent] = dad

    # recursively call self with new matrix
    # T ← NeighborJoining(D)
    tree = neighborJoin(follow, n)

    tree[i] = [parent, limbI]
    tree[j] = [parent, limbJ]

    # add found neighbors as leaves to tree
    # add two new limbs (connecting node m with leaves i and j) to the tree T
    # assign length limbLengthi to Limb(i)
    # assign length limbLengthj to Limb(j)
    # return T

    # tree will be a dictionary with keys(child nodes) going to two values, parent and distance
    return tree


def selector(star_map):
    minVal = 1000
    keyMin = 0
    yMin = 0

    for key in star_map.keys():
        row = star_map[key]
        for i in row.keys():
            if star_map[key][i] < minVal:
                minVal = star_map[key][i]
                keyMin = key
                yMin = i

    return keyMin, yMin


def dStar(grid):
    factor = len(grid) - 2
    modified = {}
    totals = {}

    for key in grid.keys():
        check = 0
        bar = grid[key]
        for index in bar.keys():
            check += bar[index]
        totals[key] = check

    for key in grid.keys():
        row = grid.get(key)
        temp = {}
        for j in row.keys():
            if row[j] == 0:
                temp[j] = 0
                continue
            value = (factor * row[j]) - totals[key] - totals[j]
            temp[j] = value
        modified[key] = temp

    return modified, totals


if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename, "r")
    lines = f.readlines()
    fixed = {}

    x = -1
    for line in lines:
        if x == -1:
            x += 1
            continue
        vals = line.strip().split(sep=" ")
        temp = {}
        y = 0
        for n in vals:
            temp[y] = int(n)
            y += 1
        fixed[x] = temp
        x += 1

    nodes = len(fixed)

    edges = neighborJoin(fixed, nodes)

    x = 0
    for node in range(len(edges.keys())):
        print(node, "->", edges[node][0], ':', edges[node][1], sep="")
        x += 1

    for node in range(len(edges.keys())):
        point = edges[node][0]
        towards = node
        dist = edges[node][1]
        print(point, "->", towards, ":", dist, sep="")
