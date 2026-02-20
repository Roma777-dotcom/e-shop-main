#!/bin/bash
set -e

echo "Starting Render build script..."

# Применяем миграции базы данных
echo "Running migrations..."
python manage.py migrate --noinput

# Собираем статические файлы
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed successfully!"

# Запускаем Gunicorn
echo "Starting Gunicorn..."
exec gunicorn shop_project.wsgi:application --bind 0.0.0.0:$PORT
