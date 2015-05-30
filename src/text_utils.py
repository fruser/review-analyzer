__author__ = 'Timur Gladkikh'

from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import string


def get_tokens(text):
    text = text.lower()
    tokens = word_tokenize(text)
    return [i for i in tokens if i not in string.punctuation]


def get_bag_of_words(word_list):
    return dict([(word, True) for word in word_list])


def get_bag_of_non_stopwords(word_list, stopfile='english'):
    exclude = stopwords.words(stopfile)
    return get_bag_of_words(set(word_list) - set(exclude))


def get_bag_of_bigrams_words(
        word_list,
        score_fn=BigramAssocMeasures.chi_sq,
        n=200):
    bigram_finder = BigramCollocationFinder.from_words(word_list)
    bigrams = bigram_finder.nbest(score_fn, n)
    return get_bag_of_words(word_list + bigrams)


def main():
    pass


if __name__ == '__main__':
    main()
