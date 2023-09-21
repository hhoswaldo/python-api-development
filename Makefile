.PHONY: install test lint build clean format type-check debug run

install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run flake8 app
	poetry run black app --check
	poetry run pylint app

type-check:
	poetry run mypy app

build:
	poetry build

clean:
	rm -rf dist
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +

format:
	poetry run black app
	poetry run isort app

debug:
	poetry run uvicorn app.__main__:app --reload

.PHONY: all
all: install lint type-check test build