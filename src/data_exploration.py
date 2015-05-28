__author__ = 'Timur Gladkikh'

from stats import get_review_sample
from file_parser import parser


def main():
    parser()
    reviews = get_review_sample()

    # users_reviews_count(reviews)                      #Result => 2088647
    # path = '../results/user_review.json'
    # json.dump(sorted_dict, open(path, 'w'))
    # reviews_count(reviews)                            #Result => 4628130

if __name__ == '__main__':
    main()
