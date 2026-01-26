.PHONY: install collectstatic migrate dev build render-start test lint format

install:
	uv sync --group dev

collectstatic:
	uv run python manage.py collectstatic --noinput

makemigrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate --noinput

dev:
	uv run python manage.py runserver

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

test:
	uv run pytest -vv

lint:
	uv run ruff check .

format:
	uv run ruff format .

# =========================
# i18n
# =========================

compilemessages:
	uv run python manage.py compilemessages

# =========================
# Rollbar
# =========================

rollbar-check:
	@uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); token = os.getenv('ROLLBAR_ACCESS_TOKEN', ''); print('ROLLBAR_ACCESS_TOKEN:', '✓' if token else '✗');"

rollbar-test:
	@echo "Testing Rollbar:"
	@echo "1. Run: make dev"
	@echo "2. Visit: http://localhost:8000/test-error/"
	@echo "3. Check Rollbar dashboard"