import sys


def createFrags(k, kmers):

    unique_kmers = []
    for kmer in kmers:
        if not unique_kmers.__contains__(kmer):
            unique_kmers.append(kmer)
    kmers.sort()
    unique_kmers.sort()
    #print(len(unique_kmers))
    added = []

    suffixes = []

    kmer_dict = {}
    safe_dict = {}
    for kmer1 in kmers:
        prefix = kmer1[:-1]
        kmer_dict[prefix] = []
        safe_dict[prefix] = []
        for matchup in kmers:
            suffix = matchup[1:]
            suffixes.append(suffix)
            if prefix == matchup[:-1]:
                kmer_dict[prefix].append(suffix)
                safe_dict[prefix].append(suffix)

    #print(kmer_dict)

    begin = ""
    end = ""
    for key,values in zip(kmer_dict.keys(), kmer_dict.values()):
        temp = key
        edges = len(values)
        for key,value in zip(kmer_dict.keys(), kmer_dict.values()):
            if value.__contains__(temp):
                edges -= 1
        if edges < 0:
            end = temp
        elif edges > 0:
            begin = temp
    if end == "":
        keys = list(kmer_dict)
        for key, values in zip(kmer_dict.keys(), kmer_dict.values()):
            for val in values:
                if val not in keys:
                    end = val

    #kmer_dict[end] = [begin]
    temp_dict = kmer_dict.copy()
    #print(kmer_dict, '\n')
    start = list(temp_dict.keys())[0]

    for key in temp_dict.keys():
        if not suffixes.__contains__(key):
            start = key
            break
        edges = 0
        edges += len(temp_dict.get(key))
        for item in temp_dict.keys():
            if temp_dict.get(item).__contains__(key):
                edges += 1
        if edges % 2 == 1:
            start = key
    cycle = [start]
    round1 = True
    notFound = True
    while notFound:
        #print(cycle)
        #print(temp_dict)
        if start in temp_dict:
            if len(temp_dict[start]) > 1:
                start = temp_dict[start].pop()
                cycle.append(start)
            elif len(temp_dict[start]) == 1:
                to_delete = start

                start = temp_dict[start].pop()
                temp_dict.pop(to_delete)
                cycle.append(start)
        else:
            for node in cycle:
                if node in temp_dict:
                    start = node
                    index = cycle.index(node)
                    beginning = cycle[0:index]
                    end = cycle[index:]
                    cycle = end + beginning
                    break
                else:
                    notFound = False
                    break

    begin_index = cycle.index(begin)
    cycle.pop()
    beginning = cycle[0:begin_index]
    end = cycle[begin_index:]
    cycle = end + beginning
    cycle = cycle[:len(kmers)]
    final_seq = ''

    #print(len(cycle))
    #print(temp_dict)

    for i in range(0, len(cycle)):
        if i == 0:
            final_seq += cycle[i]
        else:
            final_seq += cycle[i][-1]
    final_seq += safe_dict.get(cycle[len(cycle) - 1])[0][-1]
    #print(safe_dict)
    return final_seq


if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename, "r")
    lines = f.readlines()
    kmers1 = []
    kmers2 = []

    k = int(sys.argv[2])
    d = int(sys.argv[3])

    for line in lines:
        line = line.strip()
        kmers1.append(line[:k])
        kmers2.append(line[(k+1):])

    #print(kmers1, '\n')
    #print(kmers2, '\n')

    prefixText = createFrags(k, kmers1)
    #print("First: ", prefixText)

    suffixText = createFrags(k, kmers2)
    #print("Second: ", suffixText)

    #print(len(prefixText), " vs. ", len(suffixText))

    for i in range(k+d+1, len(prefixText)):
        if prefixText[i] != suffixText[i - k - d]:
            print("Strings don't match")
            break
    prefixText += suffixText[len(suffixText) - k - d:]

    print(prefixText)
