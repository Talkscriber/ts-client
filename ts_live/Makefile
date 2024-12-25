.PHONY: install test lint clean build

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=ts_live

lint:
	black .
	isort .
	flake8 .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python setup.py sdist bdist_wheel 