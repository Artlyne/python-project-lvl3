import os
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from urllib.parse import urlparse, urljoin
from page_loader import app_logger, naming, page_loader


TAGS = {'img': 'src', 'script': 'src', 'link': 'href'}
logger = app_logger.get_logger(__name__)


def is_valid(url: str, link: str) -> bool:

    if link is None:
        return False

    main_domain = urlparse(url).netloc
    file_domain = urlparse(link).netloc
    return main_domain == file_domain


def download(url: str, path: str) -> str:
    try:
        logger.info(f'getting response from {url}')
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise page_loader.AppInternalError(
            'Network error! See log for more details.') from e

    logger.info(f'creating name for {url}')
    filename = naming.create(url)
    logger.info(f'creating path for {filename}')
    filepath = os.path.join(path, filename)

    try:
        logger.info(f'writing file content to {filepath}')
        with open(filepath, 'wb') as file:
            file.write(response.content)
    except OSError as e:
        logger.error(e)
        raise page_loader.AppInternalError(
            'System error! See log for more details.') from e

    logger.info('Function done! Returning the path to the file.')
    return filepath


def replace_to_local(url: str, htmlpage: str, assets_path: str):
    logger.info('making the soup')
    soup = BeautifulSoup(htmlpage, 'html.parser')

    logger.info('looking for links')
    for resource in soup.findAll(TAGS):
        resource_source = TAGS[resource.name]
        link = urljoin(url, resource.get(resource_source))

        logger.info('checking if resource is local')
        if is_valid(url, link):
            logger.info(f'downloading {link}')
            Bar(f'Loading {link}\n')
            filepath = download(link, assets_path)
            logger.info('replacing resource path in page to local')
            resource[resource_source] = filepath

    logger.info('Function done! Returning the html page.')
    return soup.prettify(formatter='html5')
