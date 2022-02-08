import os

os.system('pip install --upgrade pip')
os.system('pip install -r requirements.txt')
os.system('python devsonly_web/manage.py shell -c "from django.core.management.utils import get_random_secret_key;'
          ' get_random_secret_key()"')
os.system('python devsonly_web/manage.py migrate')
os.system('''python devsonly_web/manage.py shell -c \
            "from django.contrib.auth import get_user_model;\
            get_user_model().objects.create_superuser('test', 'test@test.test', 'test')"''')
