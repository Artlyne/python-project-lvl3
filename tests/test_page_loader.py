from page_loader import page_loader
import pytest
import os

URL = 'https://page-loader.hexlet.repl.co'


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
    assert page_loader.make_name(tested_name) == expected_name


@pytest.mark.parametrize('url, link, expected_result', test_valid_cases)
def test_is_valid(url, link, expected_result):
    assert page_loader.is_valid(url, link) == expected_result


# def test_download():
#     """
#     я не понимаю как можно протестировать загрузку страницы, ведь актуальная
#     версия страницы может отличаться от ранее сохраненной, и это нормально
#     """
#     with open( os.getcwd() + '/tests/fixtures/expected_page.html', 'r') as f:
#         expected_page = f.read()
#
#     path_to_test_page = page_loader.download(URL, os.getcwd() + '/tests/fixtures')
#
#     with open(path_to_test_page, 'r') as f:
#         test_page = f.read()
#
#     # assert expected_page == test_page
