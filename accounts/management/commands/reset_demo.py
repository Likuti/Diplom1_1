"""Management-команда: полная очистка БД + повторный посев демо-данных.

Использование:
    python manage.py reset_demo

Удобно вызывать из Render Shell, чтобы сбросить состояние демо-стенда
к исходному. Эквивалент `flush --noinput` + `seed_demo`.
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Очищает БД и повторно заполняет её демо-данными.'

    def handle(self, *args, **options):
        self.stdout.write('Очистка таблиц (flush --noinput)...')
        call_command('flush', '--noinput')
        self.stdout.write('Посев демо-данных (seed_demo)...')
        call_command('seed_demo')
        self.stdout.write(self.style.SUCCESS('Готово: демо-стенд сброшен.'))
