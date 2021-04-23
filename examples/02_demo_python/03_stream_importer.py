import datetime
import json
import time
from random import randint

import pytz
import requests
from elasticsearch import Elasticsearch

ES_CODE_RESOURCE_ALREADY_EXISTS_EXCEPTION = 400
ES_CODE_DATA_ALREADY_EXIST = 409


def main():
    data = get_crypt_exchange_rates()
    sendJsonDataToEs(data, "0203_stream_btc_eur")


def get_crypt_exchange_rates():
    while True:
        url = "https://blockchain.info/ticker"
        r = requests.get(url)
        yield r.json()
        time.sleep(2)


def sendJsonDataToEs(lines, index):
    es = Elasticsearch()

    # 1. create MAPPING
    mapping = json.dumps({"settings": {"number_of_shards": 1, "number_of_replicas": 1}, "mappings": {"properties": _get_properties()}})

    # 2. create Index at Elasticsearch with mapping
    es.indices.create(index=index, body=mapping, ignore=[ES_CODE_RESOURCE_ALREADY_EXISTS_EXCEPTION])

    # 3. upload csv files to Elasticsearch
    for data in lines:
        l = data["EUR"]
        l["timestamp"] = str(pytz.timezone(time.tzname[0]).localize(datetime.datetime.now()).isoformat())
        l["last_fake"] = float(l["last"]) + float(l["last"]) * (float(randint(0, 30) / 100))
        print(l)
        es.create(index=index, id=_get_hash(l), body=l, ignore=[ES_CODE_DATA_ALREADY_EXIST], request_timeout=10)


def _get_hash(l):
    # create hash from unique field combinations
    return str(l["timestamp"])


def _get_properties():
    return {
        "timestamp": {
            "type": "date"
        },
        "15m": {
            "type": "float"
        },
        "last": {
            "type": "float"
        },
        "last_fake": {
            "type": "float"
        },
        "buy": {
            "type": "float"
        },
        "sell": {
            "type": "float"
        },
        "symbol": {
            "type": "keyword"
        },
    }


if __name__ == '__main__':
    main()
