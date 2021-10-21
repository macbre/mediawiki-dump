init:
	pip install -e .[dev]

test:
	pytest -v

lint:
	pylint mediawiki_dump

coverage:
	pytest --cov=mediawiki_dump --cov-report=term --cov-report=xml --cov-report=html --cov-fail-under=97 -vv

.PHONY: test
