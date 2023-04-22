#!/usr/bin/env python


import os
import sys

def main():
    """
        Функция для запуска Django-приложения из командной строки.

        Использует значение переменной окружения 'DJANGO_SETTINGS_MODULE' для установки настроек Django.
        Если настройки не установлены, используется значение 'core.settings'.
        Импортирует `execute_from_command_line` из `django.core.management` для запуска командной строки Django.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
