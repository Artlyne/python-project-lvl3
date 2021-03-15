import requests
from urllib.parse import urlparse, urljoin
import re
import os
import argparse
from bs4 import BeautifulSoup


def make_name(url: str) -> str:
    # TODO заменять строку типа '_-_' на '-'
    parsed_url = urlparse(url)
    root, ext = os.path.splitext(parsed_url.path)
    name = re.sub(r'[./_]', '-', parsed_url.netloc + root)
    if not ext:
        ext += '.html'
    max_name_length = 100
    return name[:max_name_length] + ext


def download_image(url, path):
    response = requests.get(url)
    path_to_image = os.path.join(path, make_name(url))
    with open(path_to_image, 'wb') as file:
        file.write(response.content)
    return path_to_image


def replace_images(url, page, path):
    soup = BeautifulSoup(page, 'html.parser')
    for image in soup.findAll('img'):
        image_link = urljoin(url, image.get('src'))
        try:
            pos = image_link.index('?')
            image_link = image_link[:pos]
        except ValueError:
            pass
        path_to_image = download_image(image_link, path)
        image['src'] = path_to_image
    return soup.prettify(formatter='html5')


def download(url: str, path_to_save: str) -> str:
    path_to_file = os.path.join(path_to_save, make_name(url))
    path_to_images = path_to_file.rstrip('.html') + '_files'
    print(os.getcwdb())
    os.makedirs(path_to_images, exist_ok=True)
    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema:
        response = requests.get('https://' + url)
    html = replace_images(url, response.text, path_to_images)
    with open(path_to_file, 'w', encoding='utf-8') as file:
        file.write(html)
    return path_to_file


def parser():
    parser = argparse.ArgumentParser(description='web-page loader')
    parser.add_argument('url')
    parser.add_argument('--output', default=os.getcwd(),
                        help='specify path to save')
    return parser
