__author__ = 'Timur Gladkikh'
from collections import defaultdict
from operator import itemgetter
from data_loader import *

def get_review_sample():
    pickled_file = '../data/pickled/review_sample.pickle'
    if os.path.isfile(pickled_file):
        return load_pickle(pickled_file)

    parsed_file = parse()
    review_count = get_movie_vs_reviews_count(parsed_file)
    parsed_file = None   # free up memory of parsed_file
    review_count_filtered = list(review_count[x][0] for x in range(0, len(review_count)) if review_count[x][1] >= 10)

    pass


def get_users_vs_reviews_count(reviews, sort=True):
    return get_count(reviews, 'reviewerID', 'usr_review_count', sort)

def get_movie_vs_reviews_count(reviews, sort=True):
    return get_count(reviews, 'asin', 'movie_review_count', sort)

def get_count(reviews, obj, pickle_name, sort=True):
    pickled_file = '../data/pickled/{0}.pickle'.format(pickle_name)
    if os.path.isfile(pickled_file):
        return load_pickle(pickled_file)

    review_count = defaultdict(int)
    for i in range(0, len(reviews)):
        review = reviews['{0}'.format(i)]
        review_count[review['{0}'.format(obj)]] += 1

    if sort:
        review_count = sorted(review_count.items(), key=itemgetter(1), reverse=True)  # saves data as tuple

    dump_pickle(review_count, pickled_file)
    return review_count

def get_reviews_count(reviews):
    print(len(reviews))

def main():
    pass

if __name__ == '__main__':
    main()
