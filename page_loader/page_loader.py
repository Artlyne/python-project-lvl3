import requests
from urllib.parse import urlparse, urljoin
import re
import os
import argparse
from bs4 import BeautifulSoup
import logging
import sys
from progress.bar import Bar


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


tags = {'img': 'src', 'script': 'src', 'link': 'href'}


def replace_resources(url: str, page: str, path: str):
    soup = BeautifulSoup(page, 'html.parser')
    bar = Bar('Loading ', max=len(soup.findAll(tags)), suffix='%(percent)d%%')
    for resource in soup.findAll(tags):
        tag = resource.name
        link = urljoin(url, resource.get(tags[tag]))
        if is_valid(url, link):
            path_to_file = download_resource(link, path)
            resource[tags[tag]] = path_to_file
            bar.next()
        bar.finish()
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
    # if os.path.exists(path_to_page):
    #     answer = input('File already exists and will be overwritten. '
    #                    'Continue? Y/N ').lower()
    #     if answer == 'n':
    #         sys.exit()
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
