.PHONY: install test lint build clean format type-check

install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run flake8 gateway_ops
	poetry run black gateway_ops --check
	poetry run pylint gateway_ops

type-check:
	poetry run mypy gateway_ops

build:
	poetry build

clean:
	rm -rf dist
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +

format:
	poetry run black gateway_ops
	poetry run isort gateway_ops

.PHONY: all
all: install lint type-check test build