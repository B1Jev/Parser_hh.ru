# Парсер вакансий HH.ru

Это Django-приложение для парсинга вакансий с сайта hh.ru с использованием официального API HeadHunter.

## Структура проекта

- `parser_app/` - основное приложение Django
- `views.py` - представления для обработки запросов
- `models.py` - модели данных
- `parsers/hh_parser.py` - модуль для парсинга API HH.ru
- `templates/` - HTML шаблоны
- `job_parser/` - настройки проекта Django

## Установка
pip install -r requirements.txt

## Docker

docker-compose up --build

## Запуск

python manage.py migrate
python manage.py runserver
