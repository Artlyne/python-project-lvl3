import pytest
import re
import tempfile
from page_loader.page_loader import make_name, is_valid, download_resource
from page_loader.page_loader import download


URL = 'https://page-loader.hexlet.repl.co'
IMG = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'


test_names_cases = [
    (URL, 'page-loader-hexlet-repl-co.html'),
    (f'{URL}/python', 'page-loader-hexlet-repl-co-python.html'),
    (f'{URL}/python.html', 'page-loader-hexlet-repl-co-python.html'),
    (f'{URL}/python.png', 'page-loader-hexlet-repl-co-python.png'),
    (f'{URL}/python.jpg', 'page-loader-hexlet-repl-co-python.jpg'),
    (f'{URL}/python_-_1.jpg', 'page-loader-hexlet-repl-co-python-1.jpg'),
]


test_valid_cases = [
    (URL, 'https://page-loader.hexlet.repl.co/courses', True),
    (URL, 'https://hexlet.repl.co/courses', False),
    (URL, None, False),
]


@pytest.mark.parametrize('tested_name, expected_name', test_names_cases)
def test_make_name(tested_name: str, expected_name: str):
    assert make_name(tested_name) == expected_name


@pytest.mark.parametrize('url, link, expected_result', test_valid_cases)
def test_is_valid(url: str, link: str, expected_result: bool):
    assert is_valid(url, link) == expected_result


def test_download_resource():
    with open('./tests/fixtures/expected_image.png', 'rb') as expected_img:
        with tempfile.TemporaryDirectory() as tmpdirname:
            path_to_test_img = download_resource(IMG, tmpdirname)
            with open(path_to_test_img, 'rb') as test_img:
                assert bytearray(test_img.read()) == \
                       bytearray(expected_img.read())


def test_download():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open('./tests/fixtures/expected_page.html', 'r') as file:
            expected_page = re.sub(r'test', tmpdirname, file.read())
            path_to_test_page = download(URL, tmpdirname)
            with open(path_to_test_page, 'r') as test_page:
                assert expected_page == test_page.read()
