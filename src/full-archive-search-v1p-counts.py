#!/usr/bin/env python

import json
import os

import pandas as pd
import requests

bearer_token = os.environ.get('BEARER_TOKEN')
search_url = 'https://api.twitter.com/1.1/tweets/search/'
product = 'fullarchive/'  # or 30day
label = os.environ.get('TWITTER_ENV') + '/counts.json'

query_params = {
    'query': '緊急事態宣言',
    'fromDate': '202003260000',
    'toDate': '202004250000',
    'bucket': 'day',
    # 'next': None
}


def create_headers(bearer_token):
    headers = {'Authorization': 'Bearer {}'.format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request('GET', url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    headers = create_headers(bearer_token)
    url = search_url + product + label
    json_response = connect_to_endpoint(url, headers, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    data = list()
    for result in json_response['results']:
        temp = {
            'user_name': result['user']['name'],
            'text': result['text'],
            'created_at': result['created_at'],
            'geo': result['geo']
        }
        data.append(temp)
    df = pd.DataFrame.from_records(data)
    print(df.head())


if __name__ == '__main__':
    main()
