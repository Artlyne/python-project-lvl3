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
    logger.info(f'trying to download {url} to {path}')

    try:
        response = requests.get(url)
        logger.info(f'received a response from {url}')
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise page_loader.AppInternalError(
            'Network error! See log for more details.') from e

    filename = naming.create(url)
    logger.info(f'creating name for {url}')
    filepath = os.path.join(path, filename)
    logger.info(f'created path {filepath} to the page')

    try:
        with open(filepath, 'wb') as file:
            file.write(response.content)
            logger.info(f'file content written to {filepath}')
    except OSError as e:
        logger.error(e)
        raise page_loader.AppInternalError(
            'System error! See log for more details.') from e

    logger.info(f'Function done! Returning {filepath}')
    return filepath


def replace_to_local(url: str, htmlpage: str, assets_path: str):
    soup = BeautifulSoup(htmlpage, 'html.parser')
    logger.info('the soup was made')

    logger.info('looking for links')
    for resource in soup.findAll(TAGS):
        resource_source = TAGS[resource.name]
        link = urljoin(url, resource.get(resource_source))

        if is_valid(url, link):
            Bar(f'Loading {link}\n')
            filepath = download(link, assets_path)
            logger.info(f'downloaded {link}')
            resource[resource_source] = filepath
            logger.info(f'resource {resource [resource_source]} on the page '
                        f'replaced with {filepath}')

    logger.info('Function done! Returning the html page.')
    return soup.prettify(formatter='html5')
