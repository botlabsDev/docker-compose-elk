import csv
import json
from argparse import ArgumentParser
from pathlib import Path
from typing import List

import tqdm
from elasticsearch import Elasticsearch

ES_CODE_RESOURCE_ALREADY_EXISTS_EXCEPTION = 400
ES_CODE_DATA_ALREADY_EXIST = 409


def main():
    opts = _parseArgs()
    lines = readCsvFile(opts.files)
    sendCsvDataToEs(lines, index="0201_names_csv")


def _parseArgs():
    parser = ArgumentParser()
    parser.add_argument("files", type=Path, nargs="+", help="CSV files to import")
    return parser.parse_args()


def readCsvFile(files: List[Path]) -> dict:
    for file in files:
        with file.open() as f:
            reader = csv.DictReader(f)
            yield from reader


def sendCsvDataToEs(lines, index):
    es = Elasticsearch()

    # 1. create MAPPING
    mapping = json.dumps({"settings": {"number_of_shards": 1, "number_of_replicas": 1}, "mappings": {"properties": _get_properties()}})

    # 2. create Index at Elasticsearch with mapping
    es.indices.create(index=index, body=mapping)

    # 3. upload csv files to Elasticsearch
    for l in tqdm.tqdm(lines):
        es.create(index=index, id=_get_hash(l), body=l, ignore=[ES_CODE_DATA_ALREADY_EXIST], request_timeout=10)


def _get_hash(l):
    # create hash from unique field combinations
    return str(l["Surname"] + l["GivenName"])


def _get_properties():
    return {
        "Age": {
            "type": "long"
        },
        "Centimeters": {
            "type": "long"
        },
        "Color": {
            "type": "keyword"
        },
        "Company": {
            "type": "keyword"
        },
        "EmailAddress": {
            "type": "keyword"
        },
        "Gender": {
            "type": "keyword"
        },
        "GivenName": {
            "type": "keyword"
        },
        "Kilograms": {
            "type": "double"
        },
        "Latitude": {
            "type": "double"
        },
        "Longitude": {
            "type": "double"
        },
        "Occupation": {
            "type": "text"
        },
        "Surname": {
            "type": "keyword"
        },
        "Title": {
            "type": "keyword"
        },
        "ZipCode": {
            "type": "long"
        },
        "location": {
            "type": "geo_point"
        }
    }


if __name__ == '__main__':
    main()
