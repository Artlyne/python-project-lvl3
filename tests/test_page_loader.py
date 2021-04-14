import os
import tempfile
from page_loader import page_loader


URL = 'https://artlyne.github.io/python-project-lvl3'
NAME_PREFIX = 'artlyne-github-io-python-project-lvl3'


paths = [f'/{NAME_PREFIX}_files/',
         f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-application.css',
         f'/{NAME_PREFIX}_files/artlyne-github-io-courses.html',
         f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-nodejs.png',
         f'/{NAME_PREFIX}_files/artlyne-github-io-script.js']


def test_download():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open('./tests/fixtures/expected_page.html', 'r') as expected_page:
            path_to_test_page = page_loader.download(URL, tmpdirname)
            for path in paths:
                assert os.path.exists(tmpdirname + path)
            with open(path_to_test_page, 'r') as test_page:
                assert expected_page.read() == test_page.read()
