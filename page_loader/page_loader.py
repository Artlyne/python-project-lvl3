import os
import requests
from page_loader import app_logger, resources, naming

logger = app_logger.get_logger(__name__)


class AppInternalError(Exception):
    pass


def download(url: str, path='') -> str:

    if not os.path.exists(path):
        logger.error(f"Directory {path} doesn't exists.")
        raise AppInternalError(f"Directory {path} doesn't exists.")

    try:
        logger.info(f'getting response from {url}')
        response = requests.get(url)

        if not response.ok:
            logger.error(f'Error code {response.status_code}')
            raise AppInternalError(f'Error code {response.status_code}')

    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise AppInternalError(
            'Network error! See log for more details.') from e

    logger.info(f'creating name for {url}')
    filename = naming.create(url)
    logger.info(f'creating path for {filename}')
    htmlpage_path = os.path.join(path, filename)
    logger.info('creating path for assets')
    htmlfile_extension = -5
    assets_path = htmlpage_path[:htmlfile_extension] + '_files'

    try:
        logger.info(f'creating directory {assets_path} for assets')
        os.makedirs(assets_path, exist_ok=True)
    except OSError as e:
        logger.error(e)
        raise AppInternalError(
            'System error! See log for more details.') from e

    logger.info('replacing page content to local')
    page_content = resources.replace_to_local(url, response.text, assets_path)

    try:
        logger.info(f'writing page content to {htmlpage_path}')
        with open(htmlpage_path, 'w', encoding='utf-8') as file:
            file.write(page_content)
    except OSError as e:
        logger.error(e)
        raise AppInternalError(
            'System error! See log for more details.') from e

    logger.info('Function done! Returning the path to the page.')
    return htmlpage_path
