#!/usr/bin/env python

import os
from urllib.parse import unquote

import pandas as pd
import requests

bearer_token = os.environ.get('BEARER_TOKEN')
search_url = 'https://api.twitter.com/1.1/trends/place.json'

# see https://qiita.com/hogeta_/items/8e3224c4960e19b7a33a
query_params = {'id': 1118370}  # tokyo, japan: 23424856


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
    response = connect_to_endpoint(search_url, headers, query_params)[0]
    print('trend inferred: {}'.format(response['as_of']),
          'trend oldest: {}'.format(response['created_at']),
          'location: {}'.format(response['locations'][0]['name']),
          sep='\n')
    df = pd.DataFrame.from_records(response['trends']).drop(
        ['promoted_content', 'url'], axis=1)
    df['query'] = df['query'].apply(unquote)
    print(len(df), df.head(20), sep='\n')


if __name__ == '__main__':
    main()
