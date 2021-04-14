import os
import pytest
import tempfile
from page_loader import resources

URL = 'https://artlyne.github.io/python-project-lvl3'
IMG = 'https://artlyne.github.io/python-project-lvl3/assets/nodejs.png'


@pytest.mark.parametrize('url, link, expected_result', [
    (URL, f'{URL}/courses', True),
    (URL, 'https://hexlet.github.io/courses', False),
    (URL, '/assets/image.png', True),
    (URL, 'https://github.io/python-project-lvl3/image.png', False)])
def test_is_local(url: str, link: str, expected_result: bool):
    assert resources.is_local(url, link) == expected_result


def test_download_resource():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open('./tests/fixtures/expected_image.png', 'rb') as expected_img:
            head, tail = os.path.split(tmpdirname)
            expected_path = tail + '/artlyne-github-io-python-project-lvl3-' \
                                   'assets-nodejs.png'
            test_path = resources.download(IMG, tmpdirname)
            assert expected_path == test_path
            with open(os.path.join(head, test_path), 'rb') as test_img:
                assert bytearray(expected_img.read()) == \
                       bytearray(test_img.read())
