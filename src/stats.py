__author__ = 'Timur Gladkikh'

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


def most_freq_words(db, catedory='all', rating=0, top=10):
    """
    Function for calculating most frequent words within the text block.
    :rtype : dict
    :param db: Link to the SQLite database containing sample data
    :param catedory: Filter count results by text categories. By default, 'All' categories are used
    :param rating: Filter results by the review rating score. Default is 0, i.e. 'All' scores
    :param top: Get the 'top' number of words. Defaults to 10 words
    """
    freq = defaultdict(int)
    table = db.load_table('sample')
    rows = table.all()
    for row in rows:
        freq = word_count(get_tokens(row.review_text), freq)
    return freq

def main():
    pass


if __name__ == '__main__':
    main()
