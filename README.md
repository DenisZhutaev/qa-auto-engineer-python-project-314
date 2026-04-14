### Hexlet tests and linter status:
[![Actions Status](https://github.com/DenisZhutaev/qa-auto-engineer-python-project-314/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DenisZhutaev/qa-auto-engineer-python-project-314/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DenisZhutaev_qa-auto-engineer-python-project-314&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DenisZhutaev_qa-auto-engineer-python-project-314)

## Описание проекта

Проект содержит end-to-end UI тесты для учебного Task Manager приложения на базе `pytest` и `Selenium WebDriver`.

Покрыты основные пользовательские сценарии:
- smoke-проверка доступности интерфейса;
- аутентификация и выход;
- CRUD для пользователей, статусов, меток и задач;
- базовые проверки фильтрации и изменения статуса задач на доске.

## Технологии

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- pytest
- selenium

## Запуск

Перед запуском убедитесь, что приложение доступно по адресу из `APP_BASE_URL`
(по умолчанию используется `http://localhost:5173`).

Установка зависимостей:

```bash
uv sync
```

Запуск всех тестов:

```bash
APP_BASE_URL="http://localhost:5173" make test
```

Таргеты по наборам:

- `make test-smoke`
- `make test-auth`
- `make test-users`
- `make test-statuses`
- `make test-labels`
- `make test-tasks`