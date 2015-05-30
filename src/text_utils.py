__author__ = 'Timur Gladkikh'

from _collections import defaultdict
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


def get_text_label_features(text, feature_detector=get_bag_of_bigrams_words):
    label_feats = defaultdict(list)
    for label in text.categories:
        for fileid in text.fileids(categories=[label]):
            feats = feature_detector(get_tokens(text.words(fileids=[fileid])))
            label_feats[label].append(feats)
    return label_feats


def split_label_features(lfeats, split=0.75):
    train_feats = []
    test_feats = []
    for label, feats in lfeats.items():
        cutoff = int(len(feats) * split)
        train_feats.extend([(feat, label) for feat in feats[:cutoff]])
        test_feats.extend([(feat, label) for feat in feats[cutoff:]])
    return train_feats, test_feats


def word_count(words, existing_list=None):
    result = existing_list if existing_list else defaultdict(int)
    for word in words:
        result['{0}'.format(word)] += 1
    return result


def main():
    pass


if __name__ == '__main__':
    main()
