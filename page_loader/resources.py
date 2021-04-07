import logging
import os
import requests
import sys
from bs4 import BeautifulSoup
from progress.bar import Bar
from urllib.parse import urlparse, urljoin
from page_loader import naming


TAGS = {'img': 'src', 'script': 'src', 'link': 'href'}


def is_valid(url: str, link: str) -> bool:
    if link is None:
        return False
    main_domain = urlparse(url).netloc
    file_domain = urlparse(link).netloc
    return main_domain == file_domain


def download(url: str, path: str) -> str:
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logging.error(f"Connection Error. Can't connect to: {url}")
        sys.exit()
    path_to_file = os.path.join(path, naming.create(url))
    with open(path_to_file, 'wb') as file:
        file.write(response.content)
    return path_to_file


def replace(url: str, page: str, path: str):
    soup = BeautifulSoup(page, 'html.parser')
    for resource in soup.findAll(TAGS):
        resource_source = TAGS[resource.name]
        link = urljoin(url, resource.get(resource_source))
        if is_valid(url, link):
            Bar(f'Loading {link}\n')
            path_to_file = download(link, path)
            resource[resource_source] = path_to_file
    return soup.prettify(formatter='html5')
