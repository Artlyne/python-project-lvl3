import os
import re
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from urllib.parse import urlparse, urljoin
from page_loader import app_logger, naming, page_loader


ATTRIBUTES = {'img': 'src', 'script': 'src', 'link': 'href'}
logger = app_logger.get_logger(__name__)


def download_asset(url: str, path: str) -> str:
    logger.info(f'trying to download {url} to {path}')

    try:
        response = requests.get(url)
        logger.info(f'received a response from {url}')
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise page_loader.AppInternalError(
            'Network error! See log for more details.') from e

    filename = naming.create_name(url)
    logger.info(f'created name {filename}')
    filepath = os.path.join(path, filename)
    logger.info(f'created path {filepath} to the page')

    try:
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
            logger.info(f'file content written to {filepath}')
    except OSError as e:
        logger.error(e)
        raise page_loader.AppInternalError(
            'System error! See log for more details.') from e

    _, local_dir = os.path.split(path)
    downloaded_asset_path = os.path.join(local_dir, filename)
    logger.info(f'Function done! Returning {downloaded_asset_path}')
    return downloaded_asset_path


def is_local(url: str, asset_link: str) -> bool:
    base_domain = urlparse(url).netloc
    asset_domain = urlparse(asset_link).netloc
    if not asset_domain:
        return True
    return base_domain == asset_domain


def prepare_assets(url: str, htmlpage: str, assets_path: str):
    assets = {}
    soup = BeautifulSoup(htmlpage, 'html.parser')
    for element in soup.findAll(ATTRIBUTES):
        attribute_name = ATTRIBUTES[element.name]
        asset_link = element.get(attribute_name)
        if is_local(url, asset_link):
            link = urljoin(url, asset_link)
            Bar(f'Loading {link}\n')
            downloaded_asset_path = download_asset(link, assets_path)
            assets[asset_link] = downloaded_asset_path
    return assets, soup.prettify(formatter='html5')


def replace_links(htmlpage: str, assets: dict) -> str:
    for local_asset_path, downloaded_asset_path in assets.items():
        htmlpage = re.sub(local_asset_path, downloaded_asset_path, htmlpage)

    logger.info('Function done! Returning the html page.')
    return htmlpage
