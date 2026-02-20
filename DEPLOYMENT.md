# Инструкция по развертыванию на PostgreSQL

## Развертывание на Render.com

### Автоматическое развертывание

Проект настроен для автоматического развертывания на Render.com с использованием `render.yaml`:

1. **Создайте репозиторий** на GitHub с кодом проекта
2. **Подключите репозиторий** к Render.com
3. **Render автоматически**:
   - Создаст веб-сервис и PostgreSQL базу данных
   - Установит зависимости из `requirements-prod.txt`
   - Выполнит миграции базы данных
   - Соберет статические файлы
   - Запустит Gunicorn

### Что происходит при развертывании

Скрипт `render_build.sh` выполняет следующие шаги:

1. **Миграции базы данных**
   ```bash
   python manage.py migrate --noinput
   ```

2. **Сборка статических файлов**
   ```bash
   python manage.py collectstatic --noinput --clear
   ```

3. **Запуск Gunicorn**
   ```bash
   gunicorn shop_project.wsgi:application --bind 0.0.0.0:$PORT
   ```

### Переменные окружения на Render

В `render.yaml` автоматически настраиваются:
- `DATABASE_URL` - подключение к PostgreSQL
- `SECRET_KEY` - генерируется автоматически
- `DEBUG=False` - режим продакшена
- `ALLOWED_HOSTS` - домен вашего приложения

### Логи и мониторинг

- Просмотр логов в панели Render.com
- Проверка статуса деплоя в разделе "Deployments"
- Мониторинг базы данных в разделе "Databases"

### Важно

- Убедитесь, что файл `render.yaml` и `render_build.sh` находятся в корне проекта
- `Procfile` удален (используется `render.yaml`)
- Все миграции созданы и закоммичены в репозиторий


## Настройка PostgreSQL для продакшена

### 1. Установка PostgreSQL

**Windows:**

- Скачайте установщик с <https://www.postgresql.org/download/windows/>
- Установите PostgreSQL, запомнив пароль пользователя postgres

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**

```bash
brew install postgresql
brew services start postgresql
```

### 2. Создание базы данных и пользователя

**Войдите в PostgreSQL:**
```bash
psql -U postgres
```

**Создайте базу данных и пользователя:**
```sql
CREATE DATABASE shop_db;
CREATE USER shop_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE shop_db TO shop_user;
\q
```

### 3. Настройка Django для PostgreSQL

Откройте файл `shop_project/settings.py` и измените настройки базы данных:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shop_db",
        "USER": "shop_user",
        "PASSWORD": "your_secure_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

### 4. Установка зависимостей для PostgreSQL

```bash
pip install psycopg2-binary
```

Или для продакшена (рекомендуется):
```bash
pip install psycopg2-binary
```

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Сбор статических файлов

```bash
python manage.py collectstatic
```

## Настройка для продакшена

### 1. Изменение DEBUG режима

В `shop_project/settings.py`:

```python
DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### 2. Настройка SECRET_KEY

Используйте переменную окружения для секретного ключа.

**Генерация безопасного SECRET_KEY:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Скопируйте сгенерированный ключ и добавьте его в файл `.env`:
```
DEBUG=False
SECRET_KEY=ваш-сгенерированный-ключ-здесь
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://shop_user:your_password@localhost:5432/shop_db
```

**Важно:**
- Никогда не коммитьте `.env` файл в репозиторий
- Используйте разные SECRET_KEY для разработки и продакшена
- Храните SECRET_KEY в защищённом месте в продакшене

### 3. Настройка статических файлов

Для продакшена используйте Nginx или Apache для обслуживания статических файлов.

### 4. Использование Gunicorn

Установите Gunicorn:
```bash
pip install gunicorn
```

Запуск сервера:
```bash
gunicorn shop_project.wsgi:application --bind 0.0.0.0:8000
```

### 5. Создание systemd сервиса (Linux)

Создайте файл `/etc/systemd/system/shopstore.service`:

```ini
[Unit]
Description=ShopStore Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/shop_project
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn shop_project.wsgi:application --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Запуск сервиса:
```bash
sudo systemctl start shopstore
sudo systemctl enable shopstore
```

## Резервное копирование

### Резервное копирование базы данных

```bash
pg_dump -U shop_user shop_db > backup.sql
```

### Восстановление базы данных

```bash
psql -U shop_user shop_db < backup.sql
```

## Мониторинг

### Проверка соединения с базой данных

```bash
python manage.py dbshell
```

### Проверка миграций

```bash
python manage.py showmigrations
```

## Безопасность

1. Используйте сильные пароли
2. Настройте SSL/TLS для соединения с базой данных
3. Регулярно обновляйте зависимости
4. Используйте firewall для ограничения доступа к базе данных
5. Настройте регулярное резервное копирование

## Troubleshooting

### Ошибка "connection refused"

Убедитесь, что PostgreSQL запущен:
```bash
sudo systemctl status postgresql
```

### Ошибка "FATAL: password authentication failed"

Проверьте правильность пароля пользователя в settings.py

### Ошибка "relation does not exist"

Примените миграции:
```bash
python manage.py migrate
```

## Дополнительные инструменты

### pgAdmin

Графический интерфейс для управления PostgreSQL:
- Скачайте с https://www.pgadmin.org/
- Подключитесь к серверу PostgreSQL
- Управляйте базами данных, таблицами, данными

### DBeaver

Универсальный инструмент для работы с базами данных:
- Скачайте с https://dbeaver.io/
- Поддерживает PostgreSQL и множество других баз данных
