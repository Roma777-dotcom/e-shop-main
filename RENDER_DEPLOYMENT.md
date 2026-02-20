# Деплой на Render.com

## Подготовка проекта

1. **Создайте репозиторий на GitHub**
   - Загрузите весь проект в новый репозиторий GitHub

2. **Настройте переменные окружения в render.yaml**
   - Файл `render.yaml` уже настроен для деплоя

## Деплой через Render.com

### Вариант 1: Автоматический деплой через GitHub

1. **Зарегистрируйтесь на [Render.com](https://render.com)**
   - Создайте аккаунт через GitHub

2. **Подключите репозиторий**
   - В панели Render нажмите "New +"
   - Выберите "Web Service"
   - Подключите ваш GitHub репозиторий
   - Render автоматически найдет файл `render.yaml`

3. **Настройте сервис**
   - Имя: `shopstore` (или любое другое)
   - Region: Frankfurt или ближайший к вам
   - Plan: Free

4. **База данных**
   - Render автоматически создаст PostgreSQL базу данных
   - Переменная `DATABASE_URL` будет автоматически добавлена

5. **Запустите деплой**
   - Нажмите "Create Web Service"
   - Render выполнит:
     - Установку зависимостей из `requirements-prod.txt`
     - Миграции базы данных
     - Сборку статических файлов
     - Запуск приложения

### Вариант 2: Ручной деплой через render.yaml

1. **Установите Render CLI**
   ```bash
   npm install -g render-cli
   ```

2. **Авторизуйтесь**
   ```bash
   render login
   ```

3. **Задеплойте проект**
   ```bash
   render deploy
   ```

## После деплоя

1. **Получите URL вашего сайта**
   - В панели Render найдите URL вашего сервиса
   - Пример: `https://shopstore.onrender.com`

2. **Обновите ALLOWED_HOSTS**
   - Добавьте ваш URL в `render.yaml`:
   ```yaml
   ALLOWED_HOSTS: shopstore.onrender.com
   ```

3. **Перезадеплойте** для применения изменений

## Мониторинг и логи

- **Логи**: В панели Render → Logs
- **Метрики**: В панели Render → Metrics
- **База данных**: В панели Render → Databases

## Возможные проблемы

### Ошибка: ModuleNotFoundError: No module named 'dotenv'
**Решение**: Добавьте `python-dotenv` в requirements.txt (уже добавлен)

### Ошибка: Static files not found
**Решение**: Убедитесь, что `whitenoise` установлен и настроен в settings.py

### Ошибка: Database connection failed
**Решение**: Проверьте, что переменная `DATABASE_URL` настроена в Render

## Локальная разработка

1. **Скопируйте .env.example в .env**
   ```bash
   cp .env.example .env
   ```

2. **Настройте переменные окружения в .env**

3. **Запустите сервер**
   ```bash
   python manage.py runserver
   ```

## Полезные команды

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Сборка статических файлов
python manage.py collectstatic

# Создание суперпользователя
python manage.py createsuperuser
```

## Структура проекта для Render

```
/
├── Procfile                    # Команды запуска
├── render.yaml                 # Конфигурация Render
├── requirements-prod.txt       # Зависимости для продакшена
├── .env.example               # Пример переменных окружения
├── .gitignore                 # Исключения из Git
├── shop_project/
│   ├── settings.py            # Настройки Django
│   ├── wsgi.py                # WSGI приложение
│   └── urls.py                # URL маршруты
├── accounts/                  # Приложение аккаунтов
├── shop/                      # Приложение магазина
├── cart/                      # Приложение корзины
├── orders/                    # Приложение заказов
├── pages/                     # Приложение страниц
├── static/                    # Статические файлы
├── templates/                 # Шаблоны
└── media/                     # Медиа файлы
```
