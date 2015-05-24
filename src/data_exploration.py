__author__ = 'Timur Gladkikh'
from utils import *

def main():
    reviews = get_review_sample()

    # users_reviews_count(reviews)                      #Result => 2088647
    # path = '../results/user_review.json'
    # json.dump(sorted_dict, open(path, 'w'))
    # reviews_count(reviews)                            #Result => 4628130

if __name__ == '__main__':
    main()
