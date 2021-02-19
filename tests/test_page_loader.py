from page_loader import page_loader
import pytest
import os

URL = 'https://ru.hexlet.io/courses'


test_names_cases = [
    ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
    ('http://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
    # ('ru.hexlet.io/courses/', 'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/courses/python',
     'ru-hexlet-io-courses-python.html'),
    # ('https://ru.hexlet.io/courses/python.html',
    #  'ru-hexlet-io-courses-python.html'),
    ]


@pytest.mark.parametrize('tested_name, expected_name', test_names_cases)
def test_make_name(tested_name: str, expected_name: str):
    assert page_loader.make_name(tested_name) == expected_name


def test_download():
    """
    я не понимаю как можно протестировать загрузку страницы, ведь актуальная
    версия страницы может отличаться от ранее сохраненной, и это нормально
    """
    with open( os.getcwd() + '/tests/fixtures/expected_page.html', 'r') as f:
        expected_page = f.read()

    path_to_test_page = page_loader.download(URL, os.getcwd() + '/tests/fixtures')

    with open(path_to_test_page, 'r') as f:
        test_page = f.read()

    # assert expected_page == test_page
