import pytest
from page_loader import naming


URL = 'https://artlyne.github.io/python-project-lvl3'
NAME_PREFIX = 'artlyne-github-io-python-project-lvl3'


@pytest.mark.parametrize('tested_name, expected_name', [
    (URL, f'{NAME_PREFIX}.html'),
    (f'{URL}/python', f'{NAME_PREFIX}-python.html'),
    (f'{URL}/python.html', f'{NAME_PREFIX}-python.html'),
    (f'{URL}/python.png', f'{NAME_PREFIX}-python.png'),
    (f'{URL}/python.jpg', f'{NAME_PREFIX}-python.jpg'),
    (f'{URL}/python%1.jpg', f'{NAME_PREFIX}-python-1.jpg')])
def test_make_name(tested_name: str, expected_name: str):
    assert naming.create(tested_name) == expected_name
