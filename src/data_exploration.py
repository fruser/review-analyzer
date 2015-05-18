__author__ = 'Timur Gladkikh'
from collections import defaultdict
import json
from data_loader import *

def users_reviews_count(reviews):
    path = '../results/user_review.json'
    usr_review = defaultdict(int)
    for i in range(0, len(reviews)):
        review = reviews['{0}'.format(i)]
        usr_review[review['reviewerID']] += 1
    json.dump(usr_review, open(path, 'w'))


def reviews_count(reviews):
    print(len(reviews))


def main():
    path = '../data/sample_file.json.gz'
    reviews = parse(path)
    users_reviews_count(reviews)                      #Result => 2088647
    reviews_count(reviews)                            #Result => 4628130

if __name__ == '__main__':
    main()
