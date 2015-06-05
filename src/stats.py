__author__ = 'Timur Gladkikh'

import operator
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from nltk.classify.util import accuracy
import nltk
from file_parser import *
from text_utils import *


def get_review_sample(db, size=20):
    """
    Creates review sample from the dataset and stores it within the database under the
    `sample` table. Each row also contains review category based on the assigned star rating
    :param db: Reference to the SQLite dataset file
    :param size: Number of reviews per user required in order to be included into the sample
    :return: Returns reference to the sample database
    """
    if db['sample'] is not None:
        return db

    categories = {
        'positive': 'rating > 3',
        'neutral': 'rating = 3',
        'negative': 'rating < 3'
    }
    with db as tx:
        for category in categories:
            sql = 'SELECT * ' \
                  'FROM reviews ' \
                  'WHERE {0} ' \
                  'GROUP BY reviewer_id ' \
                  'HAVING COUNT(*) >= {1}'.format(categories[category], size)
            result = db.query(sql)
            for row in result:
                tx['sample'].insert(dict(
                    reviewer_id=row.reviewer_id,
                    movie=row.movie,
                    review_text=row.review_text,
                    rating=row.rating,
                    category=category
                ))
    create_index(db)
    return db


def most_freq_words(db, category='all', rating=0, rem_stopwords=True, top=10):
    """
    Function for calculating most frequent words within the text block.
    :rtype : list
    :param db: Link to the SQLite database containing sample data
    :param category: Filter count results by text categories. By default, 'All' categories are used
    :param rating: Filter results by the review rating score. Default is 0, i.e. 'All' scores
    :param rem_stopwords: Exclude stopwords from the calculations
    :param top: Get the 'top' number of words. Defaults to 10 words
    """
    freq = defaultdict(int)
    sql = 'SELECT * FROM sample ' \
        if category == 'all' and rating == 0 \
        else 'SELECT * FROM sample WHERE '

    if category != 'all':
        sql += ' category=\'{0}\' '.format(category)
    if rating > 0:
        if 'category' in sql:
            sql += ' AND '
        sql += ' rating={0} '.format(rating)

    rows = db.query(sql)
    for row in rows:
        tokens = get_tokens(row.review_text, rem_stopwords=True) if rem_stopwords else get_tokens(row.review_text)
        freq = word_count(tokens, freq)

    return sorted(freq.items(), key=operator.itemgetter(1), reverse=True)[0:top]


def log_regression_classifier(train_features):
    sk_classifier = SklearnClassifier(LogisticRegression())
    return sk_classifier.train(train_features)


def naive_bayes_classifier(train_features):
    sk_classifier = SklearnClassifier(MultinomialNB())
    return sk_classifier.train(train_features)


def get_precision_recall_fmeasure(classifier, test_features):
    ref_sets = defaultdict(set)
    test_sets = defaultdict(set)
    ref_conf_matrix = []
    test_conf_matrix = []
    precisions = {}
    recalls = {}
    fmeasure = {}
    conf_matrix = {}

    for i, (features, label) in enumerate(test_features):
        ref_sets[label].add(i)
        observed = classifier.classify(features)
        test_sets[observed].add(i)
        ref_conf_matrix.append(label)
        test_conf_matrix.append(observed)

    for label in classifier.labels():
        precisions[label] = nltk.metrics.precision(ref_sets[label], test_sets[label])
        recalls[label] = nltk.metrics.recall(ref_sets[label], test_sets[label])
        fmeasure[label] = nltk.metrics.f_measure(ref_sets[label], test_sets[label])
        conf_matrix = nltk.metrics.ConfusionMatrix(ref_conf_matrix, test_conf_matrix)

    return precisions, recalls, fmeasure, conf_matrix


def model_test(classifier, test_features):
    print('Model Accuracy: {0}'.format(accuracy(classifier, test_features)))
    precisions, recalls, f_measure, conf_matrix = get_precision_recall_fmeasure(classifier, test_features)
    print('Precisions: {0}'.format(precisions))
    print('Recalls: {0}'.format(recalls))
    print('F-Measure: {0}'.format(f_measure))
    print('Confusion Matrix: {0}'.format(conf_matrix))


def main():
    pass


if __name__ == '__main__':
    main()
