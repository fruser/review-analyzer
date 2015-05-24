__author__ = 'Timur Gladkikh'
import gzip
import os
import pickle

def parse():
    path = '../data/reviews_Movies_and_TV.json.gz'
    pickled_file = '../data/pickled/reviews.pickle'
    if os.path.isfile(pickled_file):
        return load_pickle(pickled_file)

    line_num = 0
    parsed = {}
    with gzip.open(path, 'rb') as f:
        for line in f:
            parsed['{0}'.format(line_num)] = eval(line)
            line_num += 1

    dump_pickle(parsed, pickled_file)
    return parsed

def dump_pickle(obj, file):
    if not os.path.isfile(file):
        with open(file, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_pickle(file):
    if os.path.isfile(file):
        with open(file, 'rb') as f:
            data = pickle.load(f)
        return data

def main():
    pass

if __name__ == '__main__':
    main()
