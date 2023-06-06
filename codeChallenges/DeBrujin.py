import sys

def createFrags(seq, num):
    length = len(seq)
    last = length - num
    kmers = []
    kmers2 = []

    for i in range(0, last + 1):
        frag = ""
        for j in range(0, num):
            frag += seq[i + j]
        if not kmers.__contains__(frag):
            kmers.append(frag)
        kmers2.append(frag)
        kmers2.sort()
    added = []
    kmers.sort()
    for kmer1 in kmers:
        preffix1 = kmer1[:-1]
        temp = []
        for kmer2 in kmers2:
            preffix = kmer2[:-1]
            suffix2 = kmer2[1:]
            if preffix1 == preffix:
                temp.append(suffix2)
        kmers_final = ",".join(temp)
        if not added.__contains__(preffix1):
            print(preffix1 + " -> " + kmers_final)
        added.append(preffix1)
    return


if __name__ == '__main__':
    createFrags(sys.argv[1], int(sys.argv[2]))