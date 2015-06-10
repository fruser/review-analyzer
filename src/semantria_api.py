__author__ = 'Timur Gladkikh'

import semantria
import time
import yaml
import ssl
from stats import *
from utils import *


RESULTS_DIR = '../results/semantria/'


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
    last_row = 0

    existing_files = [os.path.splitext(filename)[0] for filename in get_files(RESULTS_DIR)]
    if len(existing_files) > 0:
        last_row = sorted([int(str(filename).replace('semantria_api_', '')) for filename in existing_files],
                          reverse=True)[0]
    for row in rows:
        if len(existing_files) > 0:
            if row.id <= last_row:
                continue

        if len(row.review_text) >= 8191:
            row.review_text = shorten_text(row.review_text)

        if len(row.review_text) == 0:
            continue

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
                    print(row.id)
                    batch = 0
                    results = {}
                    uuid_obj = []
                    time.sleep(3)
                    break
                elif status is None or int(status) > 300:
                    print(status)
                    continue
        else:
            batch += 1


def main():
    api_key, secret_key = get_keys()
    db = get_review_sample(parser())
    api_analyzer(api_key, secret_key, db)

    db_result, api_result = merge_files(RESULTS_DIR)
    conf_matrix = nltk.metrics.ConfusionMatrix(db_result, api_result)
    print(conf_matrix)


if __name__ == '__main__':
    main()
