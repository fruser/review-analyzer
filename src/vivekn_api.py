__author__ = 'Timur Gladkikh'

from stats import *
from utils import *


def combine_response_result(result, response):
    for i in range(0, len(response)):
        result[i]['api_result'] = response[i]['result'].lower()
        result[i]['confidence'] = response[i]['confidence']
    return result


def main():
    results_dir = '../results/vivekn/'
    url = 'http://sentiment.vivekn.com/api/batch/'

    db = get_review_sample(parser())
    rows = db['sample'].all()
    payload = []
    result = {}

    limit = 0
    batch = 0
    for row in rows:
        if limit == 500:
            response = post_request(payload, url)
            result = combine_response_result(result, response)

            dump_json(result, results_dir + 'vivekn_batch{0}.json'.format(batch))

            batch += 1
            payload = []
            result = {}
            limit = 0
        else:
            payload.append(row.review_text)
            result[limit] = {'category': row.category}
            limit += 1

    db_result, api_result = merge_files(results_dir)

    conf_matrix = nltk.metrics.ConfusionMatrix(db_result, api_result)
    print(conf_matrix)


if __name__ == '__main__':
    main()
