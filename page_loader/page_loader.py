import os
import requests
from page_loader import app_logger, resources, naming

logger = app_logger.get_logger(__name__)


def download(url: str, path='') -> str:
    logger.info(f'getting response from {url}')
    response = requests.get(url)

    logger.info(f'creating name for {url}')
    filename = naming.create(url)
    logger.info(f'creating path for {filename}')
    htmlpage_path = os.path.join(path, filename)
    logger.info('creating path for assets')
    assets_path = htmlpage_path.rstrip('.html') + '_files'

    logger.info(f'creating directory {assets_path}')
    os.makedirs(assets_path, exist_ok=True)

    logger.info('replacing page content to local')
    page_content = resources.replace_to_local(url, response.text, assets_path)

    logger.info(f'writing page content to {htmlpage_path}')
    with open(htmlpage_path, 'w', encoding='utf-8') as file:
        file.write(page_content)

    logger.info('Function done! Returning the path to the page.')
    return htmlpage_path
