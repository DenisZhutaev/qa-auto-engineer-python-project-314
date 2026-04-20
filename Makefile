.PHONY: start test coverage-xml test-smoke test-auth test-users test-statuses test-labels test-tasks

start:
	python3 main.py

test:
	uv run pytest

coverage-xml:
	uv run pytest --cov=tests --cov-report=xml

test-smoke:
	uv run pytest -k smoke

test-auth:
	uv run pytest -k auth

test-users:
	uv run pytest -k users

test-statuses:
	uv run pytest -k statuses

test-labels:
	uv run pytest -k labels

test-tasks:
	uv run pytest -k tasks
