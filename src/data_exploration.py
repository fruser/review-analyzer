__author__ = 'Timur Gladkikh'

from stats import *
from file_parser import parser


def main():
    sample = get_review_sample(parser())
    freq_words = most_freq_words(sample, rem_stopwords=False)
    freq_no_stop_words = most_freq_words(sample)
    print(freq_words)
    print(freq_no_stop_words)


if __name__ == '__main__':
    main()
