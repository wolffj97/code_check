import sys


class Node:
    id = ""
    children = {}

    def __init__(self, id_val):
        self.id = id_val
        self.children = {}


def Trie(patterns):
    tree = []
    root = Node(0)
    tree.append(root)
    counter = 1
    for string in patterns:
        location = root
        for letter in string:
            if letter in location.children.keys():
                location = location.children[letter]
                continue
            else:
                x = Node(counter)
                counter += 1
                location.children[letter] = x
                tree.append(x)
                location = x
    return tree


if __name__ == "__main__":

    filename = sys.argv[1]
    f = open(filename, "r")
    lines = f.readlines()
    new_lines = []
    for line in lines:
        line = line.strip().split(' ')
        for item in line:
            new_lines.append(item)
    print(new_lines)
    tree = Trie(new_lines)

    '''target = tree[1]
    for i in target.children.keys():
        print(target.id, target.children[i].id, i)'''

    for item in tree:
        id = item.id
        for child in item.children.keys():
            print(id, item.children[child].id, child)
