# Django JSON-RPC Project

Этот проект представляет собой Django-приложение, которое использует JSON-RPC для взаимодействия с удаленным API. Он настроен для работы с Docker и Poetry.

## Структура проекта

- `Dockerfile`: Файл для сборки Docker-образа.
- `docker-compose.yml`: Файл для оркестрации Docker-контейнеров.
- `pyproject.toml`: Файл конфигурации Poetry.
- `settings.py`: Файл настроек Django.

## Требования

- Python 3.11
- Django 
- Poetry
- Docker
- Docker Compose


## Установка

1. **Клонирование репозитория**:

    ```bash
    git https://github.com/samsegomof/jrpc_django_task.git
    cd test_project
    ```

2. **Установка зависимостей с помощью Poetry**:

    Убедитесь, что у вас установлен Poetry. Если нет, следуйте инструкциям на [официальном сайте Poetry](https://python-poetry.org/docs/#installation).
   (Poetry автоматически создаст виртуальное окружение при установке зависимостей.)

    ```bash
    poetry install
    ```

## Запуск проекта в Docker

1. **Сборка Docker-образа**:

    ```bash
    docker-compose build --no-cache
    ```

2. **Запуск контейнеров**:

    ```bash
    docker-compose up
    ```

3. Приложение будет доступно по адресу `http://localhost:8000`.

## Использование JSON-RPC

Пример вызова метода `auth.check` через форму на главной странице.


## Переменные окружения

В файле `docker-compose.yml` установлены переменные окружения для управления конфигурацией проекта. Для настройки среды переменные можно изменить или добавить новые в секции `environment`.

## Настройка SSL сертификатов

Для использования двустороннего TLS (SSL) необходимо настроить сертификаты и ключи в `settings.py`.

Пример конфигурации:

```python
# settings.py

JSON_RPC_API_URL = 'https://slb.medv.ru/api/v2/'
JSON_RPC_API_CERT = """
-----BEGIN CERTIFICATE-----
... ваш сертификат ...
-----END CERTIFICATE-----
"""
JSON_RPC_API_KEY = """
-----BEGIN PRIVATE KEY-----
... ваш ключ ...
-----END PRIVATE KEY-----
"""
