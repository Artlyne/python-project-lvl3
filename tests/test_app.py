from page_loader import app


def test_download():
    assert app.download() == 'Yo'
