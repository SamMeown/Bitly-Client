import os
import requests
from typing import Optional
from urllib.parse import urlparse


def get_user_info() -> Optional[dict]:
    url = 'https://api-ssl.bitly.com/v4/user'
    token = os.getenv('GENERAL_TOKEN')
    if not token:
        return None
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def shorten_link(token: str, long_url: str) -> Optional[str]:
    if not token:
        return None
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'long_url': long_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()['link']


def count_clicks(token: str, link: str) -> Optional[int]:
    if not token:
        return None
    parsed = urlparse(link)
    bitlink = '{}{}'.format(parsed.netloc, parsed.path)
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'.format(bitlink=bitlink)
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'unit': 'day', 'units': -1}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(token: str, link: str) -> bool:
    parsed = urlparse(link)
    bitlink = '{}{}'.format(parsed.netloc, parsed.path)
    url = 'https://api-ssl.bitly.com/v4/expand'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'bitlink_id': bitlink}
    response = requests.post(url, headers=headers, json=payload)

    return response.ok


if __name__ == '__main__':
    access_token = os.getenv('GENERAL_TOKEN')
    url = input('Enter url: ')
    try:
        if is_bitlink(access_token, url):
            try:
                print('Bitlink has been clicked {} time(s)'.format(count_clicks(access_token, url)))
            except requests.exceptions.HTTPError as error:
                if error.response.status_code == 403:
                    print(f'Failed to count clicks via Bitly: No access to this bitlink')
                else:
                    raise
        else:
            try:
                print('Bitlink: {}'.format(shorten_link(access_token, url)))
            except requests.exceptions.HTTPError as error:
                if error.response.status_code == 400:
                    print(f'Failed to shorten link via Bitly: Invalid url')
                else:
                    raise
    except requests.exceptions.RequestException as error:
        print(f'An error occured during request:\n{error}')