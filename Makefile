install:
		poetry build
		pip install --user dist/*.whl

lint:
		poetry run flake8 page_loader
