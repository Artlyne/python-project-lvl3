import argparse
import os
import re
import sys
import logging
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from urllib.parse import urlparse, urljoin


TAGS = {'img': 'src', 'script': 'src', 'link': 'href'}


def make_name(url: str) -> str:
    parsed_url = urlparse(url)
    root, ext = os.path.splitext(parsed_url.path)
    name = re.sub(r'_-_|[./_]', '-', parsed_url.netloc + root)
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
        sys.exit()
    path_to_file = os.path.join(path, make_name(url))
    with open(path_to_file, 'wb') as file:
        file.write(response.content)
    return path_to_file


def replace_resources(url: str, page: str, path: str):
    soup = BeautifulSoup(page, 'html.parser')
    for resource in soup.findAll(TAGS):
        resource_source = TAGS[resource.name]
        link = urljoin(url, resource.get(resource_source))
        if is_valid(url, link):
            Bar(f'Loading {link}\n')
            path_to_file = download_resource(link, path)
            resource[resource_source] = path_to_file
    return soup.prettify(formatter='html5')


def download(url: str, path: str) -> str:
    # TODO добавить проверку корректности введеных данных
    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - '
                               '%(message)s - %(filename)s - '
                               'function %(funcName)20s()'
                        )
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logging.error(f"Connection Error. Can't connect to: {url}")
        sys.exit()
    logging.info('making file name')
    path_to_page = os.path.join(path, make_name(url))
    path_to_files = path_to_page.rstrip('.html') + '_files'
    logging.info(f'Creating directory {path_to_files}')
    os.makedirs(path_to_files, exist_ok=True)
    logging.info('changing links to local resources')
    page = replace_resources(url, response.text, path_to_files)
    with open(path_to_page, 'w', encoding='utf-8') as file:
        logging.info('writing to file')
        file.write(page)
    return path_to_page


def get_args():
    parser = argparse.ArgumentParser(description='web-page loader')
    parser.add_argument('url')
    parser.add_argument('--output', default=os.getcwd(),
                        help='specify path to save')
    return parser
