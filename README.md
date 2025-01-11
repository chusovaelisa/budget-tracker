# Budget tracker

## Запуск проекта для разработки 
- `pip install poetry` - установка poetry
- `poetry shell` - вход в виртуальное окружение 
- `poetry install` - установка зависимостей
- `python manage.py migrate` - применение миграций
- `python manage.py runserver` - запуск сервер для разработки на http://127.0.0.1:8000/
- `pip install pre-commit` - установка pre-commit hook
- `pre-commit run -a` - прогнать все линтеры
- `poetry env info` - получить информацию о виртуальном окружении (например, для настройки интерпретатора)