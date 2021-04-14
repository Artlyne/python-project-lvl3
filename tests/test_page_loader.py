import os
import tempfile
from page_loader import page_loader


URL = 'https://artlyne.github.io/python-project-lvl3'
NAME_PREFIX = 'artlyne-github-io-python-project-lvl3'
PATHS = [(f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-application.css',
         './tests/fixtures/expected_application.css'),
         (f'/{NAME_PREFIX}_files/{NAME_PREFIX}-courses.html',
          './tests/fixtures/expected_courses.html'),
         (f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-nodejs.png',
          './tests/fixtures/expected_image.png'),
         (f'/{NAME_PREFIX}_files/{NAME_PREFIX}-script.js',
          './tests/fixtures/expected_script.js')]


def test_download():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open('./tests/fixtures/expected_page.html', 'r') as expected_page:
            path_to_test_page = page_loader.download(URL, tmpdirname)

            with open(path_to_test_page, 'r') as test_page:
                assert expected_page.read() == test_page.read()

            for test_asset_path, expected_asset_path in PATHS:
                tmp_path_to_test_asset = tmpdirname + test_asset_path
                assert os.path.exists(tmp_path_to_test_asset)

                with open(tmp_path_to_test_asset, 'rb') as test_asset:
                    with open(expected_asset_path, 'rb') as expected_asset:
                        assert test_asset.read() == expected_asset.read()
