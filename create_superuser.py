import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from accounts.models import User

# Создаем суперпользователя
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@shopstore.ru',
        password='admin12345',
        first_name='Администратор',
        last_name='Системы'
    )
    print("Суперпользователь создан успешно!")
    print("Логин: admin")
    print("Пароль: admin12345")
else:
    print("Суперпользователь уже существует.")
