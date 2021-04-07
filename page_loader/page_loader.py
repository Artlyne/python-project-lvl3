import logging
import os
import sys
import requests
from page_loader import resources, naming


def download(url: str, path: str) -> str:
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
    path_to_page = os.path.join(path, naming.create(url))
    path_to_files = path_to_page.rstrip('.html') + '_files'
    logging.info(f'Creating directory {path_to_files}')
    os.makedirs(path_to_files, exist_ok=True)
    logging.info('changing links to local resources')
    page = resources.replace(url, response.text, path_to_files)
    with open(path_to_page, 'w', encoding='utf-8') as file:
        logging.info('writing to file')
        file.write(page)
    return path_to_page
