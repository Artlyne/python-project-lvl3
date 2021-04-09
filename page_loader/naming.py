import os
import re
from urllib.parse import urlparse


def create(url: str) -> str:
    parsed_url = urlparse(url)
    root, file_extension = os.path.splitext(parsed_url.path)
    name = re.sub(r'[^a-zA-Z0-9]', '-', parsed_url.netloc + root)
    if not file_extension:
        file_extension = '.html'
    max_name_length = 100
    return name[:max_name_length] + file_extension
