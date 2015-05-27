__author__ = 'Timur Gladkikh'
import data_loader

def get_review_sample():
    json_file = '../data/json/review_sample.json'
    if data_loader.os.path.isfile(json_file):
        return data_loader.load_json(json_file)

    data_loader.file_parse('reviewerID')


def main():
    pass

if __name__ == '__main__':
    main()
