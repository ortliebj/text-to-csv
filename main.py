import csv, re

def read_txt(filename):
    data = []
    no_address = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip('\n')
            #titles are the shortest line, and are ignored
            if len(line) < 35:
                continue
            else:
                if line.startswith('VEG '):
                    line = line[4:]
                    entry = split_line(line, 'VEG')
                elif line.startswith('V '):
                    line = line[2:]
                    entry = split_line(line, 'V')
                else:
                    entry = split_line(line, None)
            
            if entry[2]:
                data.append(entry)
            else:
                no_address.append(entry)

    return (data, no_address)


def split_line(line, prefix):
    #\u2014 is an m-dash
    name, line = line.split('\u2014', 1)

    # find and delete phone number
    phone = re.search(r'(\(?\d{3}\)?\s?-?\d{3}\D\d{4,5})', line)
    line = re.sub(r'(\(?\d{3}\)?\s?-?\d{3}\D\d{4,5})', '', line) 
    # find and delete website
    site = re.search(r'[a-zA-Z0-9\.\/\-]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\/\-])*', line)
    line = re.sub(r'[a-zA-Z0-9\.\/\-]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\/\-])*', '', line)

    if phone is not None:
        phone = phone.group()
    if site is not None:
        site = site.group()

    comment, address = line.split('.', 1)
    # leftovers from regex operations
    address = address.strip('. . ') 

    # prepend a label to the description
    if prefix is not None:
        comment = f'({prefix}) {comment}'

    return [name, comment, address, phone, site]


def write_to_file(filename, data):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def main():
    print('Reading your file...')
    data, no_address = read_txt('in.txt')

    print('Writing data.csv...')
    write_to_file('data.csv', data)

    print('Writing no-address.csv...')
    write_to_file('no-address.csv', no_address)

    print('Done')


if __name__ == '__main__':
    main()