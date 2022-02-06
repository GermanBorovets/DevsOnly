# Проект "DevsOnly"

### Технологический стек:
- Python 3.9
- Django 3.1+

### Инструкция по настройке проекта:
1. ` git clone https://gitlab.informatics.ru/borovec_g/only-dev.git`
2. Открыть проект в PyCharm с наcтройками по умолчанию
3. Создать виртуальное окружение (через settings -> project "devsonly" -> project interpreter)
4. Открыть терминал в PyCharm, проверить, что виртуальное окружение активировано.
5. `python initialize.py`
6. Создать конфигурацию запуска в PyCharm (файл `manage.py`, опция `runserver`)

Внимание! Создана отдельная модель пользователя в модуле `main`! 
При создании ForeignKey'ев на User'а - использовать её при помощи встроенной функции `get_user_model`.
