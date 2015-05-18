__author__ = 'Timur Gladkikh'
from collections import defaultdict
from data_loader import *

def users_reviews_count(reviews):
    usr_review = defaultdict(int)
    for i in range(0, len(reviews)):
        review = reviews['{0}'.format(i)]
        usr_review[review['reviewerID']] += 1
    return usr_review


def reviews_count(reviews):
    print(len(reviews))


def main():
    path = '../data/sample_file.json.gz'
    reviews = parse(path)
    #usr_review = users_reviews_count(reviews)      #Result => 2088647
    reviews_count(reviews)                          #Result => 4628130


if __name__ == '__main__':
    main()
