init:
	pip install -e .[dev]

test:
	pytest -v

lint:
	pylint mediawiki_dump

coverage:
	pytest --cov=mediawiki_dump --cov-report=term --cov-report=xml --cov-fail-under=91 -vv

.PHONY: test
