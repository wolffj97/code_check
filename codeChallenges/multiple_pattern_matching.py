import sys

def suffix_array(seq):
    dict = {}
    i = 0
    while len(seq) > 0:
        dict[seq] = i
        i += 1
        seq = seq[1:]
    seqs = list(dict.keys())
    indexes = list(dict.values())
    zipped = sorted(zip(seqs, indexes))
    tuples = zip(*zipped)
    list1, list2 = [list(tuple) for tuple in tuples]
    return list1,list2


if __name__ == '__main__':
    file = sys.argv[1]
    with open(file) as i:
        lines = i.read()
        lines = lines.split('\n')
    string = lines[0] + "$"
    suffixes = suffix_array(string)
    genome_list = []
    for i in range(len(string)):
        first = string[0:i]
        last = string[i:]
        new_string = last + first
        genome_list.append(new_string)

    genome_list = sorted(genome_list)
    string = ""
    for genome in genome_list:
        string += genome[-1]

    lastCol = string
    # print(lastCol)


    patterns = lines[1].split(' ')
    firstCol = ''.join(sorted(lastCol))
    subscripts = [''] * (len(lastCol))
    a_count, g_count, c_count, t_count = 0, 0, 0, 0
    a_count_2, g_count_2, c_count_2, t_count_2 = 0, 0, 0, 0
    final_dict = {}
    firstOccur = {}
    a_first, g_first, c_first, t_first = False, False, False, False
    count = [[0,0,0,0,0]]
    firstColEdit = list(firstCol)
    for i in range(len(firstCol)):
        temp = ''
        temp2 = ''
        char = firstCol[i]
        char2 = lastCol[i]
        if char == "A":
            temp += char + str(a_count)
            a_count += 1
            if not a_first:
                firstOccur["A"] = i
                a_first = True
        elif char == "G":
            temp += char + str(g_count)
            g_count += 1
            if not g_first:
                firstOccur["G"] = i
                g_first = True
        elif char == "C":
            temp += char + str(c_count)
            c_count += 1
            if not c_first:
                firstOccur["C"] = i
                c_first = True
        elif char == "T":
            temp += char + str(t_count)
            t_count += 1
            if not t_first:
                firstOccur["T"] = i
                t_first = True
        else:
            temp = "$"
            firstOccur["$"] = i
        firstColEdit[i] = temp
        tempList = count[i].copy()
        if char2 == "A":
            temp2 += char2 + str(a_count_2)
            subscripts[i] = a_count_2
            tempList[0] += 1
            a_count_2 += 1
        elif char2 == "G":
            temp2 += char2 + str(g_count_2)
            subscripts[i] = g_count_2
            tempList[1] += 1
            g_count_2 += 1
        elif char2 == "C":
            temp2 += char2 + str(c_count_2)
            subscripts[i] = c_count_2
            tempList[2] += 1
            c_count_2 += 1
        elif char2 == "T":
            temp2 += char2 + str(t_count_2)
            subscripts[i] = t_count_2
            tempList[3] += 1
            t_count_2 += 1
        else:
            temp2 = "$"
            tempList[4] += 1
        count.append(tempList)
        final_dict[temp2] = temp
    all_ans = []
    letToNum = {}
    letToNum["A"] = 0
    letToNum["G"] = 1
    letToNum["C"] = 2
    letToNum["T"] = 3
    letToNum["$"] = 4
    for pattern in patterns:
        breaked = False
        patternCopy = pattern
        top = 0
        bottom = len(lastCol) - 1
        ans = 0
        while top <= bottom:
            if len(pattern) > 0:
                symbol = pattern[-1]
                pattern = pattern[:-1]
                for i in range(top, bottom + 1):
                    if lastCol[i] == symbol:
                        top = firstOccur[symbol] + count[top][letToNum[symbol]]
                        bottom = firstOccur[symbol] + count[bottom + 1][letToNum[symbol]] - 1
                        break
                else:
                    all_ans.append(str(0))
                    breaked = True
                    break
            else:
                all_ans.append(str(bottom - top + 1))
                break
        indexList = []
        if not breaked:
            for i in range(top, bottom + 1):
                indexList.append(suffixes[1][i])
            indexList = sorted(indexList)
            indexList2 = []
            for i in indexList:
                indexList2.append(str(i))
            temp = " ".join(indexList2)
            print(patternCopy + ":" + " " + temp)
        else:
            print(patternCopy + ":")

