import argparse
import os
from typing import Optional
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def _auth_header(token: str):
    if not token:
        raise ValueError('Token is not provided or empty')
    return {'Authorization': f'Bearer {token}'}


def shorten_link(token: str, long_url: str) -> Optional[str]:
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {**_auth_header(token)}
    payload = {'long_url': long_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()['link']


def count_clicks(token: str, link: str) -> Optional[int]:
    parsed = urlparse(link)
    bitlink = '{}{}'.format(parsed.netloc, parsed.path)
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'.format(bitlink=bitlink)
    headers = {**_auth_header(token)}
    payload = {'unit': 'day', 'units': -1}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(token: str, link: str) -> bool:
    parsed = urlparse(link)
    bitlink = '{}{}'.format(parsed.netloc, parsed.path)
    url = 'https://api-ssl.bitly.com/v4/expand'
    headers = {**_auth_header(token)}
    payload = {'bitlink_id': bitlink}
    response = requests.post(url, headers=headers, json=payload)

    return response.ok


if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Simple Bitly client.'
    )
    parser.add_argument('-l', '--link', help='A link to shorten or to get info on')
    args = parser.parse_args()

    access_token = os.getenv('BC_BITLY_GENERAL_TOKEN')
    input_url = args.link or input('Enter url: ')
    if is_bitlink(access_token, input_url):
        try:
            print('Bitlink has been clicked {} time(s)'.format(count_clicks(access_token, input_url)))
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 403:
                print(f'Failed to count clicks via Bitly: No access to this bitlink')
            else:
                raise
    else:
        try:
            print('Bitlink: {}'.format(shorten_link(access_token, input_url)))
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 400:
                print(f'Failed to shorten link via Bitly: Invalid url')
            else:
                raise
