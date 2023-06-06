import sys
import copy


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
            tempRow = []
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


def dictToList(dictionary, key1, key2, node_list):
    output = []
    for node, list in dictionary.items():
        if node == key1 or node == key2:
            for entry in list:
                outputLine = node + "->" + entry
                output.append(outputLine)
                if entry != key1 and entry != key2:
                    outputLine = entry + "->" + node
                    output.append(outputLine)
        else:
            for entry in list:
                outputLine = node + "->" + entry
                output.append(outputLine)
                if entry in node_list:
                    outputLine = entry + "->" + node
                    output.append(outputLine)
    return "\n".join(output)


def generalize(tree, anchor, parents):
    brother = {}
    flipper = {}
    fixer = numLeaves
    # add leaves' parents with altered values
    for key in tree.keys():
        if tree[key][0].isalpha() and tree[key][1].isalpha():
            flipper[key] = str(fixer)
            fixer += 1

    return brother


def parsimony(rows):
    tree = {}
    reverseTree = {}
    nodes = set()

    # start with leaves and parents
    for row in rows:
        tempList = row.strip().split('->')
        nodes.add(tempList[0])
        nodes.add(tempList[1])
        if tempList[0].isalpha():
            reverseTree[tempList[0]] = tempList[1]
            if tempList[1] not in tree.keys():
                tree[tempList[1]] = [tempList[0]]
            else:
                tree[tempList[1]].append(tempList[0])

    # add parents for gen 2 nodes
    full = False
    while not full:
        for row in rows:
            tempList = row.strip().split('->')
            if tempList[1].isalpha():  # should skip the edges pointing to leaves
                continue
            elif tempList[0] in tree.keys():
                if len(tree[tempList[0]]) == 2:
                    reverseTree[tempList[0]] = tempList[1]
                    if tempList[1] not in tree.keys():
                        tree[tempList[1]] = [tempList[0]]
                    elif (tempList[0] not in tree[tempList[1]]) and len(tree[tempList[1]]) < 2:
                        tree[tempList[1]].append(tempList[0])
        if len(reverseTree.keys()) == len(nodes):
            full = True
    # change node values?
    recall = len(nodes)
    pseudo = str(recall)
    for key, val in reverseTree.items():
        if val in reverseTree.keys():
            if reverseTree[val] == key:
                tip = key
                other_side = val
                break

    reverseTree[other_side] = pseudo
    reverseTree[tip] = pseudo
    tree = {}
    for key, val in reverseTree.items():
        if val not in tree.keys():
            tree[val] = [key]
        else:
            tree[val].append(key)
    tree[pseudo] = [tip, other_side]
    nodes.add(pseudo)

    nodes = list(nodes)
    n = 0
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

    # tree = generalize(tree, pseudo, reverseTree)

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
    output = ""

    dist = totalDist
    for key, val in tree.items():
        if key == pseudo:
            continue
        for v in val:
            if not v.isalpha():
                v = finalDict[v]
            count = sum(1 for a, b in zip(v, finalDict[key]) if a != b)
            output += '\n' + v + "->" + finalDict[key] + ":" + str(count)
            output += '\n' + finalDict[key] + "->" + v + ":" + str(count)
    return [dist, output]


def swaps(edge, new_lines, matches):
    tree = {}

    node1 = edge[0]
    node2 = edge[1]
    for string in new_lines:
        tempList = string.split('->')
        if tempList[0] in tree.keys():
            tree[tempList[0]].append(tempList[1])
        else:
            tree[tempList[0]] = [tempList[1]]

    nodes_for1 = tree[node1]
    nodes_for2 = tree[node2]

    new_node1a = []
    for node in nodes_for1:
        if node != node2:
            new_node1a.append(node)

    new_node2a = []
    for node in nodes_for2:
        if node != node1:
            new_node2a.append(node)

    for node in new_node1a:
        del tree[node]

    for node in new_node2a:
        del tree[node]

    new_node1b = new_node1a.copy()
    new_node2b = new_node2a.copy()

    temp = new_node1a[0]
    new_node1a[0] = new_node2a[0]
    new_node2a[0] = temp

    temp = new_node1b[0]
    new_node1b[0] = new_node2b[1]
    new_node2b[1] = temp

    node_list = new_node1a + new_node2a

    new_node1a.append(node2)
    new_node1b.append(node2)
    new_node2a.append(node1)
    new_node2b.append(node1)

    tree_copy = copy.deepcopy(tree)

    tree[node1] = new_node1a
    tree[node2] = new_node2a
    tree_copy[node1] = new_node1b
    tree_copy[node2] = new_node2b

    zero = {}
    for key, values in tree.items():
        temp = []
        for v in values:
            if v in matches.keys():
                temp.append(matches[v])
            else:
                temp.append(v)
        if key in matches.keys():
            zero[matches[key]] = temp
        else:
            zero[key] = temp

    tree = zero

    zeta = {}
    for key, values in tree_copy.items():
        temp = []
        for v in values:
            if v in matches.keys():
                temp.append(matches[v])
            else:
                temp.append(v)
        if key in matches.keys():
            zeta[matches[key]] = temp
        else:
            zeta[key] = temp

    tree_copy = zeta
    for i in range(len(node_list)):
        if node_list[i] in matches.keys():
            node_list[i] = matches[node_list[i]]
    if node1 in matches.keys():
        node1 = matches[node1]
    if node2 in matches.keys():
        node2 = matches[node2]

    first = dictToList(tree, node1, node2, node_list)
    second = dictToList(tree_copy, node1, node2, node_list)

    return [first, second]


def toNums(chart, pairs):
    shots = []
    for bar in chart:
        bar = bar.strip().split('->')
        if bar[0] in pairs.keys():
            bar[0] = pairs[bar[0]]
        if bar[1] in pairs.keys():
            bar[1] = pairs[bar[1]]
        shots.append(str(bar[0]) + "->" + str(bar[1]))
    return shots


if __name__ == '__main__':
    file = sys.argv[1]
    with open(file) as i:
        lines = i.read()
        lines = lines.split('\n')
    numLeaves = int(lines.pop(0))

    score1, tree1 = parsimony(lines)
    print(score1, tree1, sep="")

    counter = -1
    internals = []
    matchbook = {}
    fresh = []
    for line in lines:
        tempest = line.strip().split('->')
        if tempest[0].isdigit() and tempest[1].isdigit():
            if int(tempest[0]) < int(tempest[1]):
                internals.append([tempest[0], tempest[1]])
        if tempest[0].isalpha():
            if tempest[0] not in matchbook.keys():
                counter += 1
                matchbook[tempest[0]] = str(counter)
            tempest[0] = str(matchbook[tempest[0]])
        if tempest[1].isalpha():
            if tempest[1] not in matchbook.keys():
                counter += 1
                matchbook[tempest[1]] = str(counter)
            tempest[1] = str(matchbook[tempest[1]])
        fresh.append(tempest[0] + "->" + tempest[1])

    # print(fresh)

    backtrace = {}
    for key in matchbook.keys():
        backtrace[matchbook[key]] = key
    # print(backtrace)

    improving = True
    while improving:
        alts = []
        print(internals)

        for edge in internals:
            x = swaps(edge, fresh, backtrace)
            alts.append(x[0].split('\n'))
            alts.append(x[1].split('\n'))

        compares = []
        scores = []
        # print(alts[0])
        for i in range(len(alts)):
            if i == 0:
                continue
            compares.append(parsimony(alts[i]))
            scores.append(compares[i][0])
            if i == 1:
                break
        minVal = min(scores)
        '''
        if minVal < score1:
            # print(compares[scores.index(minVal)][0])
            # print(compares[scores.index(minVal)][1])
            score1 = minVal

        else:
            improving = False
        '''
        improving = False


