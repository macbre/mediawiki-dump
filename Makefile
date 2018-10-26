init:
	pip install -e .[dev]

test:
	pytest -v

lint:
	pylint mediawiki_dump

.PHONY: test
