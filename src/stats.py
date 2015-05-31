__author__ = 'Timur Gladkikh'

import operator
from file_parser import *
from text_utils import *


def get_review_sample(db, size=20):
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


def main():
    pass


if __name__ == '__main__':
    main()
