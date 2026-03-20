# Наумкин Владимир, С01-119. Django проект для проверки устного счёта.

## Запуск проекта (инструкция для Windows)

1. Скачайте (склонируйте) репозиторий и зайдите в него из консоли (cmd)
2. python -m venv .venv
3. .venv\Scripts\activate
4. pip install -r requirements.txt
5. Создайте файл .env по подобию .env_example
6. python manage.py runserver
7. Перейдите в браузере по адресу http://127.0.0.1:8000/

## Запуск pylint

Кроме pylint установлен плагин pylint-django.

Команда pylint_run.bat запустит pylint с нужными опциями, сохранит результат в файл pylint_res.txt и выведет его содержимое на экран. Выключены проверки C0114: Missing module docstring (missing-module-docstring) и C0115: Missing class docstring (missing-class-docstring), потому что при чистом старте Django проекта эти docstring не создаются. Структура проекта стандартизована (диктуется фреймворком), docstring для своего кода я создам при необходимости.

Текущая оценка pylint: 8.95 (есть W0611 unused-import, т.к. никакого кода не написано; то указанные файлы пустые, не считая стандартных import, необходимых при их наполнении)