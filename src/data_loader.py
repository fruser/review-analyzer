__author__ = 'Timur Gladkikh'
import gzip
import os
import json

DATA_FILE = '../data/reviews_Movies_and_TV.json.gz111'
TEMP_FOLDER = '../temp/'


def file_parse(parameter):
    print(parameter)
    parsed = {}
    with gzip.open(DATA_FILE, 'rb') as f:
        for line in f:
            line = yield eval(line)

            temp_file = TEMP_FOLDER + parameter + '.json'
            if os.path.isfile(temp_file):
                line = [load_json(temp_file), line]

            parsed[line[parameter]] = line
            dump_json(parsed, temp_file)


def dump_json(obj, file):
    with open(file, 'w') as f:
        json.dump(obj, f, indent=2, sort_keys=True)


def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


def main():
    pass

if __name__ == '__main__':
    main()
