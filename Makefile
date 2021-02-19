install:
		poetry build
		pip install --user dist/*.whl

lint:
		poetry run flake8 page_loader

test:
		pytest --cov=page_loader --cov-report xml tests/

