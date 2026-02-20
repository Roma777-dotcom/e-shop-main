#!/usr/bin/env python
"""
Скрипт проверки готовности проекта к деплою на Render.com
Запустите: python pre_deploy_check.py
"""

import os
import sys
from pathlib import Path

# Цвета для вывода
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def check(condition, message):
    """Проверяет условие и выводит результат"""
    if condition:
        print(f"{Colors.GREEN}✓{Colors.END} {message}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.END} {message}")
        return False

def warn(condition, message):
    """Выводит предупреждение если условие ложно"""
    if not condition:
        print(f"{Colors.YELLOW}⚠{Colors.END} {message}")
        return False
    return True

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}=== Проверка готовности к деплою на Render ==={Colors.END}\n")
    
    all_passed = True
    
    # Проверка файлов
    print(f"{Colors.BOLD}1. Проверка файлов:{Colors.END}")
    files_to_check = [
        'render.yaml',
        'Procfile',
        'requirements.txt',
        'requirements-prod.txt',
        '.env.example',
        '.gitignore',
        'manage.py',
        'shop_project/settings.py',
        'shop_project/wsgi.py',
        'shop_project/urls.py',
    ]
    for file in files_to_check:
        if not check(Path(file).exists(), f"Файл {file} существует"):
            all_passed = False
    
    # Проверка директорий
    print(f"\n{Colors.BOLD}2. Проверка директорий:{Colors.END}")
    dirs_to_check = [
        'static',
        'media',
        'templates',
        'accounts',
        'shop',
        'cart',
        'orders',
        'pages',
    ]
    for dir_name in dirs_to_check:
        if not check(Path(dir_name).exists(), f"Директория {dir_name}/ существует"):
            all_passed = False
    
    # Проверка содержимого .gitignore
    print(f"\n{Colors.BOLD}3. Проверка .gitignore:{Colors.END}")
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        gitignore_content = gitignore_path.read_text()
        check('.env' in gitignore_content, ".env в .gitignore")
        check('db.sqlite3' in gitignore_content, "db.sqlite3 в .gitignore")
        check('__pycache__' in gitignore_content, "__pycache__ в .gitignore")
        check('.pyc' in gitignore_content, "*.pyc в .gitignore")
        check('media' in gitignore_content, "media в .gitignore")
        check('staticfiles' in gitignore_content, "staticfiles в .gitignore")
    
    # Проверка requirements-prod.txt
    print(f"\n{Colors.BOLD}4. Проверка зависимостей:{Colors.END}")
    requirements_prod_path = Path('requirements-prod.txt')
    if requirements_prod_path.exists():
        requirements_prod = requirements_prod_path.read_text()
        check('gunicorn' in requirements_prod, "gunicorn в requirements-prod.txt")
        check('whitenoise' in requirements_prod, "whitenoise в requirements-prod.txt")
        check('psycopg2' in requirements_prod or 'psycopg2-binary' in requirements_prod, 
              "psycopg2 в requirements-prod.txt")
        check('dj-database-url' in requirements_prod, "dj-database-url в requirements-prod.txt")
        check('python-dotenv' in requirements_prod, "python-dotenv в requirements-prod.txt")
    
    # Проверка settings.py
    print(f"\n{Colors.BOLD}5. Проверка настроек Django:{Colors.END}")
    settings_path = Path('shop_project/settings.py')
    if settings_path.exists():
        settings_content = settings_path.read_text()
        check('dj_database_url' in settings_content, "dj-database-url импортирован")
        check('load_dotenv' in settings_content, "python-dotenv настроен")
        check('DEBUG' in settings_content and 'os.environ' in settings_content,
              "DEBUG из переменных окружения")
        check('SECRET_KEY' in settings_content and 'os.environ' in settings_content,
              "SECRET_KEY из переменных окружения")
        check('ALLOWED_HOSTS' in settings_content and 'os.environ' in settings_content,
              "ALLOWED_HOSTS из переменных окружения")
        check('WhiteNoiseMiddleware' in settings_content, "Whitenoise в MIDDLEWARE")
        check('STATIC_ROOT' in settings_content, "STATIC_ROOT настроен")
        check('MEDIA_ROOT' in settings_content, "MEDIA_ROOT настроен")
        check('DATABASE_URL' in settings_content or 'dj_database_url.config' in settings_content,
              "База данных через DATABASE_URL")
        
        # Проверка security настроек для продакшена
        warn('if not DEBUG:' in settings_content, 
             "Security настройки для продакшена (рекомендуется)")
    
    # Проверка render.yaml
    print(f"\n{Colors.BOLD}6. Проверка render.yaml:{Colors.END}")
    render_yaml_path = Path('render.yaml')
    if render_yaml_path.exists():
        render_yaml = render_yaml_path.read_text()
        check('type: web' in render_yaml, "Тип сервиса: web")
        check('env: python' in render_yaml, "Окружение: python")
        check('gunicorn' in render_yaml, "Gunicorn в startCommand")
        check('DATABASE_URL' in render_yaml, "DATABASE_URL настроен")
        check('SECRET_KEY' in render_yaml, "SECRET_KEY настроен")
        check('DEBUG' in render_yaml and 'False' in render_yaml, "DEBUG: False")
        check('ALLOWED_HOSTS' in render_yaml, "ALLOWED_HOSTS настроен")
        check('databases:' in render_yaml, "База данных настроена")
    
    # Проверка Procfile
    print(f"\n{Colors.BOLD}7. Проверка Procfile:{Colors.END}")
    procfile_path = Path('Procfile')
    if procfile_path.exists():
        procfile_content = procfile_path.read_text()
        check('web:' in procfile_content, "web процесс определен")
        check('gunicorn' in procfile_content, "Gunicorn используется")
        check('release:' in procfile_content, "release процесс определен")
    
    # Проверка .env.example
    print(f"\n{Colors.BOLD}8. Проверка .env.example:{Colors.END}")
    env_example_path = Path('.env.example')
    if env_example_path.exists():
        env_example = env_example_path.read_text()
        check('SECRET_KEY' in env_example, "SECRET_KEY в .env.example")
        check('DEBUG' in env_example, "DEBUG в .env.example")
        check('ALLOWED_HOSTS' in env_example, "ALLOWED_HOSTS в .env.example")
        check('DATABASE_URL' in env_example, "DATABASE_URL в .env.example")
    
    # Проверка наличия .env (предупреждение)
    print(f"\n{Colors.BOLD}9. Проверка безопасности:{Colors.END}")
    warn(not Path('.env').exists(), 
         "Файл .env не существует (хорошо - он в .gitignore)")
    
    # Проверка Git
    print(f"\n{Colors.BOLD}10. Проверка Git:{Colors.END}")
    if Path('.git').exists():
        check(True, "Git репозиторий инициализирован")
        # Проверка наличия коммитов
        result = os.system('git rev-parse HEAD >nul 2>&1')
        if result == 0:
            check(True, "Git имеет коммиты")
        else:
            warn(False, "Git не имеет коммитов - сделайте первый коммит")
            all_passed = False
    else:
        warn(False, "Git репозиторий не инициализирован")
        all_passed = False
    
    # Итог
    print(f"\n{Colors.BOLD}{'='*50}{Colors.END}")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ Проект готов к деплою!{Colors.END}")
        print(f"\n{Colors.BLUE}Следующие шаги:{Colors.END}")
        print("1. git add .")
        print("2. git commit -m 'Ready for Render deployment'")
        print("3. Создайте репозиторий на GitHub")
        print("4. git push")
        print("5. Подключите репозиторий на render.com")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Проект не готов к деплою{Colors.END}")
        print(f"\n{Colors.YELLOW}Исправьте отмеченные ошибки перед деплоем{Colors.END}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
