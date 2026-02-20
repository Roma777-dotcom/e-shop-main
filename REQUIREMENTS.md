# Зависимости проекта

## Файлы требований

### requirements.txt
Основные зависимости для работы проекта.

**Установка:**
```bash
pip install -r requirements.txt
```

**Содержит:**
- Django и DRF
- PostgreSQL драйвер
- Pillow для изображений
- django-crispy-forms для форм
- django-filter для фильтрации
- Базовые инструменты для продакшена

### requirements-dev.txt
Зависимости для разработки.

**Установка:**
```bash
pip install -r requirements-dev.txt
```

**Содержит:**
- Все зависимости из requirements.txt
- django-debug-toolbar для отладки
- Инструменты качества кода (flake8, black, isort, pylint)
- Фреймворки для тестирования (pytest)
- Инструменты для документации

### requirements-prod.txt
Зависимости для продакшен-среды.

**Установка:**
```bash
pip install -r requirements-prod.txt
```

**Содержит:**
- Все зависимости из requirements.txt
- gunicorn как WGI сервер
- whitenoise для статических файлов
- Инструменты для мониторинга и логирования
- Инструменты для кэширования и оптимизации

## Использование

### Локальная разработка
```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux/Mac)
source venv/bin/activate

# Установка зависимостей для разработки
pip install -r requirements-dev.txt
```

### Продакшен
```bash
# Установка зависимостей для продакшена
pip install -r requirements-prod.txt
```

## Обновление зависимостей

Для обновления всех зависимостей до последних версий:

```bash
pip install --upgrade -r requirements.txt
```

## Проверка зависимостей

Для проверки установленных пакетов:

```bash
pip list
```

Для проверки устаревших пакетов:

```bash
pip list --outdated
```

## Замораживание зависимостей

Для создания списка всех установленных пакетов с точными версиями:

```bash
pip freeze > requirements-freeze.txt
```

## Описание основных зависимостей

### Core
- **Django** - веб-фреймворк
- **djangorestframework** - REST API для Django

### База данных
- **psycopg2-binary** - драйвер PostgreSQL

### Изображения
- **Pillow** - работа с изображениями

### Формы и фильтры
- **django-crispy-forms** - рендеринг форм
- **django-filter** - фильтрация QuerySet

### Продакшен
- **gunicorn** - WGI сервер
- **whitenoise** - обслуживание статических файлов
- **python-decouple** - управление настройками

### Разработка
- **django-debug-toolbar** - панель отладки
- **flake8** - проверка кода
- **black** - форматирование кода
- **pytest** - тестирование

### Дополнительно
- **celery** - асинхронные задачи
- **redis** - брокер сообщений
- **django-anymail** - отправка email
- **drf-yasg** - документация API

## Безопасность

Регулярно обновляйте зависимости для исправления уязвимостей безопасности:

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

Используйте `pip-audit` для проверки безопасности:

```bash
pip install pip-audit
pip-audit
```
