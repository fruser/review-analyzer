__author__ = 'Timur Gladkikh'

import requests
from stats import *
import nltk


def post_request(payload):
    url = 'http://sentiment.vivekn.com/api/batch/'
    return json.loads(requests.post(url, data=json.dumps(payload)).text)


def combine_response_result(result, response):
    for i in range(0, len(response)):
        result[i]['api_result'] = response[i]['result'].lower()
        result[i]['confidence'] = response[i]['confidence']
    return result


def main():
    results_dir = '../results/vivekn/'

    '''
    db = get_review_sample(parser())
    rows = db['sample'].all()
    payload = []
    result = {}

    limit = 0
    batch = 0
    for row in rows:
        if limit == 500:
            response = post_request(payload)
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
    '''

    files = [file for file in os.listdir(results_dir) if os.path.isfile(results_dir + file)]

    db_result = []
    api_result = []

    for file in files:
        with open(results_dir + file) as f:
            json_data = json.load(f)
            for key in json_data.keys():
                db_result.append(json_data[key]['category'])
                api_result.append(json_data[key]['api_result'])
    conf_matrix = nltk.metrics.ConfusionMatrix(db_result, api_result)
    print(conf_matrix)


if __name__ == '__main__':
    main()
