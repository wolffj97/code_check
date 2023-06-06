import sys
import copy


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


if __name__ == "__main__":

    filename = sys.argv[1]
    f = open(filename, "r")
    lines = f.readlines()
    new_lines = []
    for line in lines:
        line = line.strip()
        new_lines.append(line)

    tree = {}
    edge = new_lines[0].split(sep=" ")

    node1 = edge[0]
    node2 = edge[1]
    for string in new_lines[1:]:
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

    print(dictToList(tree, node1, node2, node_list), "\n")
    print(dictToList(tree_copy, node1, node2, node_list))



