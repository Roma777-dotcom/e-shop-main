# Быстрый деплой на Render.com

## Подготовка

1. **Загрузите проект на GitHub**
   - Создайте новый репозиторий
   - Загрузите все файлы проекта

2. **Зарегистрируйтесь на [Render.com](https://render.com)**
   - Используйте GitHub аккаунт для авторизации

## Деплой

### Способ 1: Через веб-интерфейс

1. Перейдите на [dashboard.render.com](https://dashboard.render.com)
2. Нажмите **"New +"** → **"Web Service"**
3. Подключите ваш GitHub репозиторий
4. Render автоматически найдет файл `render.yaml`
5. Нажмите **"Create Web Service"**

### Способ 2: Через CLI

```bash
# Установка Render CLI
npm install -g render-cli

# Авторизация
render login

# Деплой
render deploy
```

## После деплоя

1. Получите URL вашего сайта (пример: `https://shopstore.onrender.com`)
2. Обновите `ALLOWED_HOSTS` в `render.yaml`:
   ```yaml
   ALLOWED_HOSTS: shopstore.onrender.com
   ```
3. Перезадеплойте проект

## Файлы для деплоя

- ✅ `Procfile` - команды запуска
- ✅ `render.yaml` - конфигурация Render
- ✅ `requirements-prod.txt` - зависимости
- ✅ `.env.example` - пример переменных окружения
- ✅ `settings.py` - обновлен для продакшена

## Полная документация

Смотрите [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) для подробных инструкций.
