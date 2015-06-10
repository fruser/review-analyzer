__author__ = 'Timur Gladkikh'

import uuid
import requests
import json
import time
import os


def post_request(payload, url, json_dumps=True):
    time.sleep(2)
    payload = json.dumps(payload) if json_dumps else payload
    return json.loads(requests.post(url, data=payload).text)


def get_uuid_obj(text):
    return {'id': str(uuid.uuid4()).replace('-', ''), 'text': text}


def merge_files(results_dir):
    files = get_files(results_dir)

    db_result = []
    api_result = []

    for file in files:
        with open(results_dir + file) as f:
            json_data = json.load(f)
            for key in json_data.keys():
                db_result.append(json_data[key]['category'])
                api_result.append(json_data[key]['api_result'])
    return db_result, api_result


def get_files(local_dir):
    return [file for file in os.listdir(local_dir) if os.path.isfile(local_dir + file)]


def main():
    pass


if __name__ == '__main__':
    main()