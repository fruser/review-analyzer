__author__ = 'Timur Gladkikh'
import gzip


def parse(path):
    line_num = 0
    parsed = {}
    with gzip.open(path, 'rb') as f:
        for line in f:
            parsed['{0}'.format(line_num)] = eval(line)
            line_num += 1
    return parsed


def main():
    pass


if __name__ == '__main__':
    main()
