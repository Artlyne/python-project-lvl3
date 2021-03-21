import requests
from urllib.parse import urlparse, urljoin
import re
import os
import argparse
from bs4 import BeautifulSoup
import logging


def make_name(url: str) -> str:
    # TODO заменять строку типа '_-_' на '-'
    parsed_url = urlparse(url)
    root, ext = os.path.splitext(parsed_url.path)
    name = re.sub(r'[./_]', '-', parsed_url.netloc + root)
    if not ext:
        ext += '.html'
    max_name_length = 100
    return name[:max_name_length] + ext


def is_valid(url: str, link: str) -> bool:
    if link is None:
        return False
    main_domain = urlparse(url).netloc
    file_domain = urlparse(link).netloc
    return main_domain == file_domain


def download_resource(url: str, path: str) -> str:
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logging.error(f"Connection Error. Can't connect to: {url}")
        exit()
    path_to_file = os.path.join(path, make_name(url))
    with open(path_to_file, 'wb') as file:
        file.write(response.content)
    return path_to_file


tags = {'img': 'src', 'script': 'src', 'link': 'href'}


def replace_resources(url: str, page: str, path: str):
    soup = BeautifulSoup(page, 'html.parser')
    for resource in soup.findAll(tags):
        tag = resource.name
        link = urljoin(url, resource.get(tags[tag]))
        if is_valid(url, link):
            path_to_file = download_resource(link, path)
            resource[tags[tag]] = path_to_file
    return soup.prettify(formatter='html5')


def download(url: str, path: str) -> str:
    # TODO добавить проверку корректности введеных данных
    logging.basicConfig(filename='app.log', filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - '
                               '%(message)s - $(funcName)'
                        )
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logging.error(f"Connection Error. Can't connect to: {url}")
        exit()
    path_to_page = os.path.join(path, make_name(url))
    path_to_files = path_to_page.rstrip('.html') + '_files'
    os.makedirs(path_to_files, exist_ok=True)
    page = replace_resources(url, response.text, path_to_files)
    with open(path_to_page, 'w', encoding='utf-8') as file:
        file.write(page)
    return path_to_page


def get_args():
    parser = argparse.ArgumentParser(description='web-page loader')
    parser.add_argument('url')
    parser.add_argument('--output', default=os.getcwd(),
                        help='specify path to save')
    return parser
