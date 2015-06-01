__author__ = 'Timur Gladkikh'

from stats import *
from file_parser import parser


def main():
    sample = get_review_sample(parser())

    print('Top 10 most frequent words (stopwords included, all categories):')
    freq_words = most_freq_words(sample, rem_stopwords=False)
    print(freq_words)

    print('\nTop 10 most frequent words (stopwords not included, all categories):')
    freq_no_stop_words = most_freq_words(sample)
    print(freq_no_stop_words)

    stars = [1, 2, 3, 4, 5]
    categories = ['positive', 'neutral', 'negative']

    print('\nTop 10 most frequent words based on star ratings:')
    for star in stars:
        print('Star# ', star)
        print(most_freq_words(sample, rating=star))

    print('\nTop 10 most frequent words based on categories:')
    for category in categories:
        print('Category: ', category)
        print(most_freq_words(sample, category=category))

    temp = get_text_label_features(sample)
    train, test = split_label_features(temp)


if __name__ == '__main__':
    main()
