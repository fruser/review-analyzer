__author__ = 'Timur Gladkikh'

import gzip
import os
import json
from collections import defaultdict

DATA_FILE = '../data/reviews_Movies_and_TV.json.gz'
TEMP_FOLDER = '../temp/'


def parser(parameter):
    counts = {
        'positive': defaultdict(int),
        'neutral': defaultdict(int),
        'negative': defaultdict(int)
    }

    with gzip.open(DATA_FILE, 'rb') as f:
        for line in f:
            line = eval(line)
            obj_eval = line[parameter]

            rating = line['overall']
            rating_dir = ''

            if rating < 2.5:
                rating_dir = 'negative'
                counts['negative'][obj_eval] += 1
            elif 2.5 <= rating < 3.4:
                rating_dir = 'neutral'
                counts['neutral'][obj_eval] += 1
            elif rating >= 3.5:
                rating_dir = 'positive'
                counts['positive'][obj_eval] += 1

            review_dir = TEMP_FOLDER + rating_dir + '/'

            if not os.path.exists(review_dir):
                os.makedirs(review_dir)

            temp_file = review_dir + obj_eval + '.json'
            if os.path.isfile(temp_file):
                line = [load_json(temp_file), line]
            dump_json(line, temp_file)

    dump_json(counts, TEMP_FOLDER + 'counts.json')


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
