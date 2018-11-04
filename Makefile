coverage_options = --include='mediawiki_dump/*' --omit='test/*'

init:
	pip install -e .[dev]

test:
	pytest -v

lint:
	pylint mediawiki_dump

coverage:
	rm -f .coverage*
	rm -rf htmlcov/*
	coverage run -p -m pytest -v
	coverage combine
	coverage html -d htmlcov $(coverage_options)
	coverage xml -i
	coverage report $(coverage_options)

publish:
	# run git tag -a v0.0.0 before running make publish
	python setup.py sdist
	twine upload dist/*

.PHONY: test
