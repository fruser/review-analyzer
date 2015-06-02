__author__ = 'Timur Gladkikh'

from stats import *
from file_parser import parser


def print_results(lfeatures):
    train_set, test_set = split_label_features(lfeatures)
    classifier = scikit_learn_classifier(train_set)
    model_test(classifier, test_set)


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

    all_features = get_text_label_features(sample)

    high_info_words = get_high_information_words(all_features)
    ft_detection = lambda words: get_bad_of_words_in_set(words, high_info_words)
    lfeatures_hiw = get_text_label_features(sample, feature_detector=ft_detection)

    print_results(lfeatures_hiw)
    print_results(all_features)


if __name__ == '__main__':
    main()
