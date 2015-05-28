__author__ = 'Timur Gladkikh'

from file_parser import *


def get_review_sample():
    db = parser()

    categories = {
        'positive': 'rating >= 3.5',
        'neutral': 'rating >= 2.5 AND rating < 3.5',
        'negative': 'rating < 2.5'
    }
    with db as tx:
        for category in categories:
            sql = 'SELECT reviewer_id, movie, review_text, rating, COUNT(reviewer_id) c ' \
                  'FROM reviews ' \
                  'WHERE {0} ' \
                  'GROUP BY reviewer_id ' \
                  'ORDER BY c DESC'.format(categories[category])
            result = db.query(sql)
            for row in result:
                if row.c >= 20:
                    tx['sample'].insert(dict(
                        reviewer_id=row.reviewer_id,
                        movie=row.movie,
                        review_text=row.review_text,
                        rating=row.rating,
                        category=category,
                        count=row.c
                    ))

def main():
    pass


if __name__ == '__main__':
    main()
