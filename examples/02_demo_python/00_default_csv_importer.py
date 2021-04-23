import csv
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
    sendCsvDataToEs(lines, "0200_btc_eur")


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

    for l in tqdm.tqdm(lines):
        es.create(index=index, id=str(l), body=l, ignore=[ES_CODE_DATA_ALREADY_EXIST], request_timeout=10)


if __name__ == '__main__':
    main()
