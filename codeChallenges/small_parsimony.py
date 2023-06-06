import sys


def smallParsimony(tree, nodes, seqIndex):
    tagList = [0] * len(nodes)
    alphabet = ["A", "G", "C", "T"]
    distDict = {}
    for n in range(0, len(nodes)):
        if nodes[n].isalpha():
            tagList[n] = 1
            temp = []
            for letter in alphabet:
                if nodes[n][seqIndex] == letter:
                    temp.append(0)
                else:
                    temp.append(float('inf'))
                distDict[nodes[n]] = temp
    ripe = True
    ripeList = []
    while ripe:
        for n in range(len(nodes)):
            if tagList[n] == 0:
                children = tree[nodes[n]]
                isRipe = True
                for child in children:
                    index = nodes.index(child)
                    if tagList[index] == 0:
                        isRipe = False
                        break
                if isRipe:
                    ripeList.append(nodes[n])
        if len(ripeList) == 0:
            break
        for node in ripeList:
            index = nodes.index(node)
            tagList[index] = 1
            children = tree[node]
            minDaughter = ''
            minSon = ''
            minDaughterDist = 0
            minSonDist = 0
            i = 0
            for child in children:
                distances = distDict[child]
                minimum = min(distances)
                for d in range(len(distances)):
                    if distances[d] == minimum:
                        if i == 0:
                            minDaughter += alphabet[d]
                            minDaughterDist = minimum
                        if i == 1:
                            minSon += alphabet[d]
                            minSonDist = minimum
                i += 1
            tempRow =[]
            for letter in alphabet:
                dist = 0
                dist += minDaughterDist
                if letter not in minDaughter:
                    dist += 1
                dist += minSonDist
                if letter not in minSon:
                    dist += 1
                tempRow.append(dist)
            distDict[node] = tempRow
        ripeList = []
    return distDict







file = sys.argv[1]
with open(file) as i:
    lines = i.read()
    lines = lines.split('\n')
numLeaves = int(lines.pop(0))

tree = {}
reverseTree = {}
nodes = set()

'''for string in lines:
    tempList = string.split('->')
    if tempList[0].isalpha():
        continue
    elif not tempList[1].isalpha():
        if int(tempList[0]) < int(tempList[1]):
            continue
    if tempList[0] in tree.keys():
        tree[tempList[0]].append(tempList[1])
    else:
        tree[tempList[0]] = [tempList[1]]
    reverseTree[tempList[1]] = tempList[0]
    nodes.add(tempList[0])
    nodes.add(tempList[1])

tip = max(tree.keys())
pseudo = str(int(tip) + 1)
other_side = str(int(tip) - 1)
tree[tip] = tree[tip][0:-1]
tree[pseudo] = [tip, other_side]
reverseTree[other_side] = pseudo
reverseTree[tip] = pseudo
nodes.add(pseudo)
'''

edges = {}
scan = {}
ready = set()
for line in lines:
    x = line.strip().split('->')
    nodes.add(line[0])
    nodes.add(line[1])
    # this should add leaves and their parent in the reverse tree
    if line[0] not in edges.keys():
        edges[line[0]] = [line[1]]
    else:
        edges[line[0]].append(line[1])
    if line[1] not in edges.keys():
        edges[line[1]] = [line[0]]
    if line[0].isalpha():
        reverseTree[line[0]] = line[1]  # add [0] with parent to reverse
        if line[1] not in scan.keys():  # add parent with [0] to group of parent nodes w/children
            scan[line[1]] = [line[0]]
        else:
            scan[line[1]].append(line[0])

# loop through for adding parent nodes to existing parents
done = False
while not done:
    for node in nodes:  # add nodes to ready list
        if node in scan.keys():  # has a leaf child node already
            

nodes = list(nodes)
n = 0  # this will essentially be the number of letters/nucleotides in the strings
finalDict = {}
root = 0
for node in nodes:
    if node.isalpha():
        n = len(node)
    else:
        if int(node) > root:
            root = int(node)
        finalDict[node] = ''
seqIndex = 0
totalDist = 0

letters = ["A", "G", "C", "T"]
while n > 0:
    ans = smallParsimony(tree, nodes, seqIndex)
    counter = root
    while counter >= numLeaves:
        key = str(counter)
        value = ans[key]
        if not key.isalpha():
            minVal = min(value)
            indices = []
            index = value.index(min(value))
            for i in range(len(value)):
                if value[i] == minVal:
                    indices.append(i)
            if key == str(root):
                totalDist += min(value)
                finalDict[key] += letters[index]
            elif len(indices) > 1:
                parent = reverseTree[key]
                lastLetter = finalDict[parent][-1]
                added = False
                for i in indices:
                    if letters[i] == lastLetter:
                        finalDict[key] += lastLetter
                        added = True
                        break
                if not added:
                    finalDict[key] += letters[indices[0]]
            else:
                finalDict[key] += letters[indices[0]]
        counter -= 1
    n -= 1
    seqIndex += 1

tree[tip].append(other_side)

print(totalDist)
for key, val in tree.items():
    if key == pseudo:
        continue
    for v in val:
        if not v.isalpha():
            v = finalDict[v]
        count = sum(1 for a, b in zip(v, finalDict[key]) if a != b)
        print(v, "->", finalDict[key], ":", count, sep="")
        print(finalDict[key], "->", v, ":", count, sep="")

# print(root)
# print(totalDist)
# print(finalDict)
# print(tree)
