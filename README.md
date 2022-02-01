<<<<<<< HEAD
# Проект "DevsOnly"

### Технологический стек:
- Python 3.6
- Django 3.1+
- MySQL 

### Инструкция по настройке проекта:
1. ` git clone https://gitlab.informatics.ru/borovec_g/only-dev.git`
4. Открыть проект в PyCharm с наcтройками по умолчанию
5. Создать виртуальное окружение (через settings -> project "devsonly" -> project interpreter)
6. Открыть терминал в PyCharm, проверить, что виртуальное окружение активировано.
7. Обновить pip:
   ```bash
   pip install --upgrade pip
   ```
8. Установить в виртуальное окружение необходимые пакеты: 
   ```bash
   pip install -r requirements.txt
   ```

9. Создать уникальный ключ приложения.  
   Генерация делается в консоли Python при помощи команд:
   ```bash
   python manage.py shell -c "from django.core.management.utils import get_random_secret_key; get_random_secret_key()"
   ```
   Далее полученное значение подставляется в соответствующую переменную.
   Внимание! Без выполнения этого пункта никакие команды далее не запустятся.

10. Синхронизировать структуру базы данных с моделями: 
    ```bash
    python manage.py migrate
    ```

11. Создать суперпользователя
    ```bash
    python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('test', 'test@test.test', 'test')"
    ```

12. Создать конфигурацию запуска в PyCharm (файл `manage.py`, опция `runserver`)

Внимание! Создана отдельная модель пользователя в модуле `main`! 
При создании ForeignKey'ев на User'а - использовать её при помощи встроенной функции `get_user_model`.
=======
# Only Dev

Only Dev company
>>>>>>> ef6b893 (Initial commit)
