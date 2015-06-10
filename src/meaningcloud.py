__author__ = 'Timur Gladkikh'

import yaml
from stats import *
from utils import *


def get_api_key():
    with open('../conf/api_keys/apis.yml', 'r') as f:
        data_map = yaml.safe_load(f)
        api_key = data_map['meaningcloud']['api_key']
    return api_key


def main():
    results_dir = '../results/meaningcloud/'
    url = 'http://api.meaningcloud.com/sentiment-2.0'

    api_key = get_api_key()
    db = get_review_sample(parser())
    rows = db['sample'].all()
    result = {}

    for row in rows:
        payload = {'key': api_key,
                   'model': 'auto',
                   'txt': row.review_text}
        api_result = ''

        while True:
            try:
                response = post_request(payload, url, json_dumps=False)['score_tag']
            except KeyError:
                time.sleep(2)
                continue
            finally:
                time.sleep(2)
                break

        if response == 'P' or response == 'P+':
            api_result = 'positive'
        elif response == 'N' or response == 'N+':
            api_result = 'negative'
        elif response == 'NEU':
            api_result = 'neutral'
        result[row.id] = {'category': row.category, 'api_result': api_result}
        if row.id % 10 == 0:
            print(row.id)
            dump_json(result, results_dir + 'meaningcloud{0}.json'.format(row.id))
            result = {}

    db_result, api_result = merge_files(results_dir)
    conf_matrix = nltk.metrics.ConfusionMatrix(db_result, api_result)
    print(conf_matrix)


if __name__ == '__main__':
    main()
