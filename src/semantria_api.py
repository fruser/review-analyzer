__author__ = 'Timur Gladkikh'

import semantria
import uuid
import time
import yaml
import ssl
from stats import *


def get_uuid_obj(text):
    return {'id': str(uuid.uuid4()).replace('-', ''), 'text': text}

def get_keys():
    with open('../conf/api_keys/apis.yml', 'r') as f:
        data_map = yaml.safe_load(f)
        api_key = data_map['semantria']['api_key']
        secret_key = data_map['semantria']['api_secret']
    return api_key, secret_key


def get_api_result(session, session_length):
    results = []
    while len(results) < session_length:
        time.sleep(3)
        status = []
        while True:
            try:
                status = session.getProcessedDocuments()
                break
            except ssl.SSLError:
                continue
        results.extend(status)
    return results


# Really raw method to shorten the string
def shorten_text(text):
    return text[0:8190]


def api_analyzer(api_key, secret_key, db):
    serializer = semantria.JsonSerializer()
    session = semantria.Session(api_key, secret_key, serializer=serializer, use_compression=True)
    rows = db['sample'].all()

    results = {}
    uuid_obj = []

    batch = 0
    limit = 10

    for row in rows:
        if len(row.review_text) >= 8191:
            row.review_text = shorten_text(row.review_text)
        obj = get_uuid_obj(row.review_text)
        uuid_obj.append(obj)
        results[obj['id']] = {'category': row.category}

        if batch == limit - 1:
            while True:
                status = session.queueBatch(uuid_obj)
                if status == 202:
                    time.sleep(3)
                    api_result = get_api_result(session, limit)

                    for i in range(0, len(api_result)):
                        results[api_result[i]['id']]['api_result'] = api_result[i]['sentiment_polarity']
                    dump_json(results, '../results/semantria/semantria_api_{0}.json'.format(row.id))
                    batch = 0
                    results = {}
                    uuid_obj = []
                    time.sleep(3)
                    break
                elif status > 300:
                    print(status)
                elif status is None:
                    continue
        else:
            batch += 1


def main():
    api_key, secret_key = get_keys()
    db = get_review_sample(parser())
    api_analyzer(api_key, secret_key, db)

    results_path = '../results/semantria/'
    files = [file for file in os.listdir(results_path) if os.path.isfile(results_path + file)]

    analysis_result = {}
    for file in files:
        with open(results_path + file) as f:
            json_data = json.load(f)
            for key in json_data.keys():
                analysis_result[key] = json_data[key]
    dump_json(analysis_result, results_path + 'overall_result.json')


if __name__ == '__main__':
    main()
