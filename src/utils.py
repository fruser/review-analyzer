__author__ = 'Timur Gladkikh'
from collections import defaultdict
from operator import itemgetter
from data_loader import *

def get_review_sample(sample_size=100000, condition=20):
    json_file = '../data/json/review_sample.json'
    if os.path.isfile(json_file):
        return load_json(json_file)

    parsed_file = parse()

    count_filtered = '../data/json/review_count_filtered.json'
    if os.path.isfile(count_filtered):
        review_count_filtered = load_json(count_filtered)
    else:
        review_count = get_users_vs_reviews_count(parsed_file)
        review_count_filtered = list(review_count[x][0]
                                     for x in range(0, len(review_count)) if review_count[x][1] >= condition)
        dump_json(review_count_filtered, '../data/json/review_count_filtered.json')

    filter_list = []
    sample = {}
    for i in range(0, len(parsed_file)):
        if parsed_file['{0}'.format(i)]['reviewerID'] in review_count_filtered:
            sample['{0}'.format(i)] = parsed_file['{0}'.format(i)]
            filter_list.append(i)

    dump_json(sample, json_file)  # needs re-work
    dump_json(filter_list, '../data/json/filter_list.json')  # temporary
    return sample

def get_users_vs_reviews_count(reviews, sort=True):
    return get_count(reviews, 'reviewerID', 'usr_review_count', sort)

def get_movie_vs_reviews_count(reviews, sort=True):
    return get_count(reviews, 'asin', 'movie_review_count', sort)

def get_count(reviews, obj, json_name, sort=True):
    json_file = '../data/json/{0}.json'.format(json_name)
    if os.path.isfile(json_file):
        return load_json(json_file)

    review_count = defaultdict(int)
    for i in range(0, len(reviews)):
        review = reviews['{0}'.format(i)]
        review_count[review['{0}'.format(obj)]] += 1

    if sort:
        review_count = sorted(review_count.items(), key=itemgetter(1), reverse=True)  # saves data as tuple

    dump_json(review_count, json_file)
    return review_count

def main():
    pass

if __name__ == '__main__':
    main()
