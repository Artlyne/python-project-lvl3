import os
import requests
from page_loader import app_logger, resources, naming

logger = app_logger.get_logger(__name__)


class AppInternalError(Exception):
    pass


def download(url: str, path='') -> str:
    logger.info(f'trying to download {url} to {path}')

    if not os.path.exists(path):
        logger.error(f"Directory {path} doesn't exists.")
        raise AppInternalError(f"Directory {path} doesn't exists.")

    try:
        response = requests.get(url)
        logger.info(f'received a response from {url}')

        if response.raise_for_status():
            logger.error(f'Error code {response.status_code}')
            raise AppInternalError(f'Error code {response.status_code}')

    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise AppInternalError(
            'Network error! See log for more details.') from e

    filename = naming.create_name(url)
    logger.info(f'created name {filename}')
    htmlpage_path = os.path.join(path, filename)
    logger.info(f'created path {htmlpage_path} to the page')

    assets_dir_name = naming.create_assets_path_name(url)
    logger.info(f'created assets dir name {assets_dir_name}')
    assets_path = os.path.join(path, assets_dir_name)
    logger.info(f'created path {assets_path} for assets')

    try:
        os.makedirs(assets_path, exist_ok=True)
        logger.info(f'created directory {assets_path} for assets')
    except OSError as e:
        logger.error(e)
        raise AppInternalError(
            'System error! See log for more details.') from e

    assets = resources.prepare_assets(url, response.text, assets_path)
    htmlpage = resources.replace_links(response.text, assets)
    logger.info('all page content replaced to local')

    try:
        with open(htmlpage_path, 'w', encoding='utf-8') as file:
            file.write(htmlpage)
            logger.info(f'page content written to {htmlpage_path}')
    except OSError as e:
        logger.error(e)
        raise AppInternalError(
            'System error! See log for more details.') from e

    logger.info(f'Function done! Returning {htmlpage_path}')
    return htmlpage_path
