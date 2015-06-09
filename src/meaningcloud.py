__author__ = 'Timur Gladkikh'

import requests
from stats import *
import yaml
import nltk
import time


def post_request(payload):
    url = 'http://api.meaningcloud.com/sentiment-2.0'
    time.sleep(2)
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

        while True:
            try:
                response = post_request(payload)['score_tag']
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
        result[row.id] = {'db_result': row.category, 'api_result': api_result}
        if row.id % 10 == 0:
            print(row.id)
            dump_json(result, results_dir + 'meaningcloud{0}.json'.format(row.id))
            result = {}

    files = [file for file in os.listdir(results_dir) if os.path.isfile(results_dir + file)]

    db_result = []
    api_result = []

    for file in files:
        with open(results_dir + file) as f:
            json_data = json.load(f)
            for key in json_data.keys():
                db_result.append(json_data[key]['db_result'])
                api_result.append(json_data[key]['api_result'])
    conf_matrix = nltk.metrics.ConfusionMatrix(db_result, api_result)
    print(conf_matrix)


if __name__ == '__main__':
    main()
