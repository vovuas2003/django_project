# Наумкин Владимир, С01-119. Django проект MathMaster для проверки устного счёта.

## Запуск проекта (инструкция для Windows)

0. Установите Python (я запускал на 3.12.2)
1. Скачайте (склонируйте) репозиторий и зайдите в него из консоли (cmd)
2. python -m venv .venv
3. .venv\Scripts\activate
4. pip install -r requirements.txt
5. Создайте файл .env по подобию .env_example
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py createsuperuser
9. python manage.py runserver
10. Перейдите в браузере по адресу http://127.0.0.1:8000/ (админка по адресу http://127.0.0.1:8000/admin/ но админ не является полноценным пользователем сайта - нет профиля)

## Запуск pylint

Кроме pylint установлен плагин pylint-django.

Команда pylint_run.bat запустит pylint с нужными опциями, сохранит результат в файл pylint_res.txt и выведет его содержимое на экран. Выключены проверки C0114: Missing module docstring (missing-module-docstring) и C0115: Missing class docstring (missing-class-docstring), потому что при чистом старте Django проекта эти docstring не создаются. Структура проекта стандартизована (диктуется фреймворком), docstring для своего кода я создам при необходимости.

Текущая оценка pylint: 9.35