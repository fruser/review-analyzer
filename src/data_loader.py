__author__ = 'Timur Gladkikh'
import gzip
import os
import pickle
import json

DATA_FILE = '../data/reviews_Movies_and_TV.json.gz'

def parse():
    json_file = '../data/json/reviews.json'
    if os.path.isfile(json_file):
        return load_json(json_file)

    line_num = 0
    parsed = {}
    with gzip.open(DATA_FILE, 'rb') as f:
        for line in f:
            parsed['{0}'.format(line_num)] = eval(line)
            line_num += 1

    dump_json(parsed, json_file)
    return parsed

def parse_strict_json():
    json_file = '../data/json/reviews_strict.json'
    if os.path.isfile(json_file):
        return load_json(json_file)

    line_num = 0
    parsed = {}
    with gzip.open(DATA_FILE, 'rb') as f:
        for line in f:
            yield json.dump(eval(line))

    dump_json(parsed, json_file)
    return parsed

def dump_json(obj, file):
    if not os.path.isfile(file):
        with open(file, 'w') as f:
            json.dump(obj, f, indent=2, sort_keys=True)

def load_json(file):
    if os.path.isfile(file):
        with open(file, 'r') as f:
            data = json.load(f)
        return data

def main():
    pass

if __name__ == '__main__':
    main()
