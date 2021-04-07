import os
import re
from urllib.parse import urlparse


def create(url: str) -> str:
    parsed_url = urlparse(url)
    root, ext = os.path.splitext(parsed_url.path)
    name = re.sub(r'_-_|[./_]', '-', parsed_url.netloc + root)
    if not ext:
        ext += '.html'
    max_name_length = 100
    return name[:max_name_length] + ext
