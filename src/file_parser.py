__author__ = 'Timur Gladkikh'

import gzip
import json
import dataset
import os
from stuf import stuf

DATA_FILE = '../data/reviews_Movies_and_TV.json.gz'
DB_FILE = '../data/dataset.db'
DB_URL = 'sqlite:///{0}'.format(DB_FILE)

def parser():
    if os.path.isfile(DB_FILE):
        return dataset.connect(DB_URL, row_type=stuf)

    db = dataset.connect(DB_URL)
    with gzip.open(DATA_FILE, 'rb') as f:
        with db as tx:
            for line in f:
                data = eval(line)
                tx['reviews'].insert(dict(
                    reviewer_id=data['reviewerID'],
                    movie=data['asin'],
                    review_text=data['reviewText'],
                    rating=data['overall']
                ))

    table = db['reviews']
    table.create_index(['reviewer_id', 'rating'])
    table.create_index(['rating'])
    table.create_index(['reviewer_id'])


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
