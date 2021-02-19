import requests
from urllib.parse import urlparse
import re
import os
import argparse


def make_name(url: str) -> str:
    parsed_url = urlparse(url)
    name = re.sub(r'[./]', '-', parsed_url.netloc + parsed_url.path)
    return f'{name}.html'


def make_dir(path: str) -> str:
    current_dir = os.getcwd()
    os.makedirs(current_dir + path, exist_ok=True)
    return current_dir + path


def download(url: str, path_to_save: str) -> str:
    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema:
        response = requests.get('https://' + url)

    path_to_file = make_dir(path_to_save) + '/' + make_name(url)

    with open(f'{path_to_file}', 'w') as f:
        f.write(response.text)

    return path_to_file


def parser():
    parser = argparse.ArgumentParser(description='web-page loader')
    parser.add_argument('url')
    parser.add_argument('--output', default='', help='specify path to save')
    return parser
