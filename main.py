import csv

def read_txt(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip('\n')
            if len(line) < 35:
                continue
            else:
                if line.startswith('VEG '):
                    line = line[4:]
                elif line.startswith('V '):
                    line = line[2:]
                
                tmp = line.split('\u2014', 1)
                name = tmp[0]
                details = tmp[1].split('.', 3)

                data.append([name if j == 0 else details[j-1] for j in range(5)])

    return data


def write_to_file(filename, data):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def main():
    data = read_txt('directory.txt')
    write_to_file('out.csv', data)
    


if __name__ == '__main__':
    main()
