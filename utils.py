def read_classification_from_file(file_name):
    dict = {}
    with open(file_name, "r", encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            line = line.split()
            dict.get(line[0])
            dict[line[0]] = line[1]
    return dict


def write_classification_to_file(file_name):
    dict = read_classification_from_file('Text.txt')
    with open(file_name, "w", encoding='utf-8') as f:
        for keys, values in dict.items():
            f.write(str(keys) + ' ' + str(values) + '\n')
