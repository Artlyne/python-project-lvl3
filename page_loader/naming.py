import os
import re
from urllib.parse import urlparse

MAX_LENGTH = 100


def create_name(url: str) -> str:
    parsed_url = urlparse(url)
    root, file_extension = os.path.splitext(parsed_url.path)
    name = re.sub(r'[^a-zA-Z0-9]', '-', parsed_url.netloc + root)
    if not file_extension:
        file_extension = '.html'
    return name[:MAX_LENGTH] + file_extension


def create_assets_dir_name(url: str) -> str:
    parsed_url = urlparse(url)
    root, _ = os.path.splitext(parsed_url.path)
    name = re.sub(r'[^a-zA-Z0-9]', '-', parsed_url.netloc + root)
    return name[:MAX_LENGTH] + '_files'
