import json

import tqdm
from elasticsearch import Elasticsearch
from shodan import Shodan

ES_CODE_RESOURCE_ALREADY_EXISTS_EXCEPTION = 400
ES_CODE_DATA_ALREADY_EXIST = 409

API_KEY = "<API KEY>"


def main():
    data = get_ip_data_from_shodan(API_KEY)
    sendJsonDataToEs(data, "2004444odan_data")


def get_ip_data_from_shodan(api_key):
    api = Shodan(api_key)
    # https://developer.shodan.io/api

    # search = 'scada country:"DE"'
    # search = "s7-300 country:'DE'"  ## Siemens SIMATIC S7-300 (maybe Honeypots)
    search = "Wasserwerk"
    # search = "flowChief"
    # search = "http.title:'Secure Access SSL VPN' country:'DE'"  ## PulseSecure, maybe CVE-2021-2289

    print("Query shodan ...")
    data = api.search(query=search)
    for d in tqdm.tqdm(data["matches"]):
        yield d


def sendJsonDataToEs(lines, index):
    es = Elasticsearch()

    # 1. create MAPPING
    mapping = json.dumps({"settings": {"number_of_shards": 3, "number_of_replicas": 3}})

    # 2. create Index at Elasticsearch with mapping
    es.indices.create(index=index, body=mapping, ignore=[ES_CODE_RESOURCE_ALREADY_EXISTS_EXCEPTION])

    # 3. upload csv files to Elasticsearch
    for l in lines:
        l = _clean_fields(l)
        es.create(index=index, id=l["_shodan"]["id"], body=l, ignore=[ES_CODE_DATA_ALREADY_EXIST], request_timeout=10)

        
def _clean_fields(l):
    forbidden_fields = ["vulns",  ## Field is to long
                        "_id",    ## Field [_id] is a metadata field and cannot be added inside a document.
                        ]

    for field in forbidden_fields:
        if field in l:
            l.pop(field)
    try:
        l["ssl"]["cert"]["serial"] = ""
    except KeyError:
        pass
    return l


def _get_hash(l):
    # create hash from unique field combinations
    return str(l["timestamp"])

if __name__ == '__main__':
    main()
