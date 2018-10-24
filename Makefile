init:
	pip install pipenv && pipenv install --dev

test:
	pipenv run pytest -v

lint:
	pylint corpus/ *.py

.PHONY: test
