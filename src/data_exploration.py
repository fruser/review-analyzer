__author__ = 'Timur Gladkikh'

from stats import *
from file_parser import parser


def main():
    sample = get_review_sample(parser())
    freq_words = most_freq_words(sample)


if __name__ == '__main__':
    main()
