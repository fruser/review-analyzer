__author__ = 'Timur Gladkikh'

from file_parser import *


def get_review_sample(size=20):
    db = parser()

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


def main():
    pass


if __name__ == '__main__':
    main()
