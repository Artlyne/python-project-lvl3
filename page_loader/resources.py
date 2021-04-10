import os
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from urllib.parse import urlparse, urljoin
from page_loader import app_logger, naming, page_loader


TAGS = {'img': 'src', 'script': 'src', 'link': 'href'}
logger = app_logger.get_logger(__name__)


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
    logger.info(f'created name for {url}')
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


def is_local(url: str, asset_link: str) -> bool:
    base_domain = urlparse(url).netloc
    asset_domain = urlparse(asset_link).netloc
    if not asset_domain:
        return True
    return base_domain == asset_domain


def replace_to_local(url: str, htmlpage: str, assets_path: str):
    soup = BeautifulSoup(htmlpage, 'html.parser')
    logger.info('the soup was made')

    logger.info('looking for links')
    for asset in soup.findAll(TAGS):
        tag = TAGS[asset.name]
        asset_link = asset.get(tag)

        if is_local(url, asset_link):
            link = urljoin(url, asset_link)
            Bar(f'Loading {link}\n')
            local_link = download(link, assets_path)
            logger.info(f'downloaded {link}')
            asset[tag] = local_link
            logger.info(f'asset {link} on the page replaced with {local_link}')

    logger.info('Function done! Returning the html page.')
    return soup.prettify(formatter='html5')
