import os
import pytest
import re
import tempfile
from page_loader import naming, page_loader, resources


URL = 'https://artlyne.github.io/python-project-lvl3'
IMG = 'https://artlyne.github.io/python-project-lvl3/assets/nodejs.png'
NAME_PREFIX = 'artlyne-github-io-python-project-lvl3'


test_names_cases = [
    (URL, f'{NAME_PREFIX}.html'),
    (f'{URL}/python', f'{NAME_PREFIX}-python.html'),
    (f'{URL}/python.html', f'{NAME_PREFIX}-python.html'),
    (f'{URL}/python.png', f'{NAME_PREFIX}-python.png'),
    (f'{URL}/python.jpg', f'{NAME_PREFIX}-python.jpg'),
    (f'{URL}/python%1.jpg', f'{NAME_PREFIX}-python-1.jpg'),
]


test_local_cases = [
    (URL, f'{URL}/courses', True),
    (URL, 'https://hexlet.github.io/courses', False),
    (URL, '/assets/image.png', True),
    (URL, 'https://github.io/python-project-lvl3/image.png', False),
]


paths = [f'/{NAME_PREFIX}_files/',
         f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-application.css',
         f'/{NAME_PREFIX}_files/artlyne-github-io-courses.html',
         f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-nodejs.png',
         f'/{NAME_PREFIX}_files/artlyne-github-io-script.js']


@pytest.mark.parametrize('tested_name, expected_name', test_names_cases)
def test_make_name(tested_name: str, expected_name: str):
    assert naming.create(tested_name) == expected_name


@pytest.mark.parametrize('url, link, expected_result', test_local_cases)
def test_is_local(url: str, link: str, expected_result: bool):
    assert resources.is_local(url, link) == expected_result


def test_download_resource():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open('./tests/fixtures/expected_image.png', 'rb') as expected_img:
            expected_path = tmpdirname + f'/{NAME_PREFIX}-assets-nodejs.png'
            test_path = resources.download(IMG, tmpdirname)
            assert expected_path == test_path
            with open(test_path, 'rb') as test_img:
                assert bytearray(expected_img.read()) == \
                       bytearray(test_img.read())


def test_download():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open('./tests/fixtures/expected_page.html', 'r') as file:
            expected_page = re.sub(r'test', tmpdirname, file.read())
            path_to_test_page = page_loader.download(URL, tmpdirname)
            for path in paths:
                assert os.path.exists(tmpdirname + path)
            with open(path_to_test_page, 'r') as test_page:
                assert expected_page == test_page.read()
