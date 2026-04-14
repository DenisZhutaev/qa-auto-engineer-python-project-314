.PHONY: start test test-smoke test-auth test-users test-statuses test-labels test-tasks

start:
	python3 main.py

test:
	uv run pytest

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
