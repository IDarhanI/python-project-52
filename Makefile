.PHONY: install dev start build migrate collectstatic test lint render-start

install:
	uv sync

dev:
	uv run python manage.py runserver

start:
	uv run gunicorn task_manager.wsgi

build:
	./build.sh

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

test:
	uv run python manage.py test

lint:
	uv run ruff check .

render-start:
	gunicorn task_manager.wsgi