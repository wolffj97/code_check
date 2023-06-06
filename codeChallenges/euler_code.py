#print(cycle)
        print(temp_dict)
        if start in temp_dict:
            if len(temp_dict[start]) > 1:
                start = temp_dict[start].pop()
                cycle.append(start)
            elif len(temp_dict[start]) == 1:
                to_delete = start
                if round1:
                    start = temp_dict.get(start)[0]
                else:
                    start = temp_dict[start].pop()
                    temp_dict.pop(to_delete)
                round1 = False
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