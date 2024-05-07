from dotenv import load_dotenv
import requests
import os
import argparse
from urllib.parse import urlparse


def shorten_link(token, long_url):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api-ssl.bitly.com/v4/shorten"

    params = {"long_url": long_url}
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(token, bitlink):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"

    params = {"unit": "month", "units": "-1"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(token, bitlink):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"

    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.environ['BITLY_TOKEN']

    parser = argparse.ArgumentParser(description='Videos to images')
    parser.add_argument('--url', type=str, help='Input dir for videos')
    args = parser.parse_args()
    parsed_url = urlparse(args.url)
    parsed_url = f"{parsed_url.netloc}{parsed_url.path}"
    try:
        if is_bitlink(token, parsed_url):
            print("Количество кликов: ", count_clicks(token, parsed_url))
        else:
            bitlink = shorten_link(token, args.url)
            print("Битлинк", bitlink)
    except requests.exceptions.HTTPError:
        print("Ошибка при отправке запроса")


if __name__ == "__main__":
    main()
