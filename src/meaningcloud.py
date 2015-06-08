__author__ = 'Timur Gladkikh'

import requests
from stats import *
import yaml
import nltk
import time


def post_request(payload):
    url = 'http://api.meaningcloud.com/sentiment-2.0'
    time.sleep(1.5)
    return json.loads(requests.post(url, data=payload).text)


def get_api_key():
    with open('../conf/api_keys/apis.yml', 'r') as f:
        data_map = yaml.safe_load(f)
        api_key = data_map['meaningcloud']['api_key']
    return api_key


def main():
    results_dir = '../results/meaningcloud/'
    api_key = get_api_key()

    db = get_review_sample(parser())
    rows = db['sample'].all()
    result = {}

    for row in rows:
        payload = {'key': api_key,
                   'model': 'auto',
                   'txt': row.review_text}
        api_result = ''
        try:
            response = post_request(payload)['score_tag']
        except:
            response = ''

        if response == 'P' or response == 'P+':
            api_result = 'positive'
        elif response == 'N' or response == 'N+':
            api_result = 'negative'
        elif response == 'NEU':
            api_result = 'neutral'
        result[row.id] = {'db_result': row.category, 'api_result': api_result}
        if row.id % 10 == 0:
            dump_json(result, results_dir + 'meaningcloud{0}.json'.format(row.id))


if __name__ == '__main__':
    main()
