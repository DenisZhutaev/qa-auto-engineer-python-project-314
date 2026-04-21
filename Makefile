.PHONY: install start check lint test test-coverage coverage-xml test-smoke test-auth test-users test-statuses test-labels test-tasks

install:
	uv sync --group dev

start:
	docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

check:
	$(MAKE) lint
	$(MAKE) test

lint:
	uv run ruff check .

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=tests --cov-report=xml tests/

coverage-xml:
	$(MAKE) test-coverage

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
