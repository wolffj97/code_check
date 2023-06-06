
# Press the green button in the gutter to run the script.
import sys

if __name__ == '__main__':
    file = sys.argv[1]
    with open(file) as i:
        lines = i.read()
        lines = lines.split('\n')
    string = lines[0]

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

    print(string)

