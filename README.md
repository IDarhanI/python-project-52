### Hexlet tests and linter status:
[![Actions Status](https://github.com/IDarhanI/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/IDarhanI/python-project-52/actions)

# Task Manager - Python Project 52

Проект менеджера задач на Django.

## Локальная разработка

1. Клонируйте репозиторий
2. Установите uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Скопируйте `.env.example` в `.env` и настройте переменные
4. Установите зависимости: `make install`
5. Выполните миграции: `make migrate`
6. Запустите сервер: `make dev`

## Деплой

Проект развернут на Render.com: [https://your-app-name.onrender.com](https://your-app-name.onrender.com)

## Команды

- `make install` - установить зависимости
- `make dev` - запустить сервер разработки
- `make start` - запустить с gunicorn
- `make migrate` - выполнить миграции
- `make collectstatic` - собрать статику
- `make test` - запустить тесты
- `make lint` - проверить код линтером