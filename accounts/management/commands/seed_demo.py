"""Команда seed_demo: создаёт демонстрационные данные.

Использование:
    python manage.py seed_demo

Создаёт три учётные записи (admin/head/teacher), две группы, нескольких
сотрудников, воспитанников и записи посещаемости.
"""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from attendance.models import AttendanceRecord
from children.models import Child, Parent
from groups.models import Group
from staff.models import Employee

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу демонстрационными данными.'

    @transaction.atomic
    def handle(self, *args, **options):
        if Group.objects.exists():
            self.stdout.write(self.style.WARNING('Демоданные уже есть, пропускаю.'))
            return

        g1 = Group.objects.create(
            name='Ромашка', age_category='3-4 года',
            direction='общеразвивающая', max_capacity=20,
        )
        g2 = Group.objects.create(
            name='Звёздочка', age_category='5-6 лет',
            direction='общеразвивающая', max_capacity=22,
        )

        teacher_emp = Employee.objects.create(
            last_name='Петрова', first_name='Анна', patronymic='Сергеевна',
            position='Воспитатель', qualification='Высшая категория',
            education='Высшее педагогическое', experience_years=12,
            phone='+79991112233', email='petrova@example.org',
            group=g1, hire_date=date(2018, 9, 1),
        )
        Employee.objects.create(
            last_name='Сидорова', first_name='Елена', patronymic='Ивановна',
            position='Воспитатель', qualification='Первая категория',
            education='Высшее педагогическое', experience_years=7,
            phone='+79992223344', group=g2, hire_date=date(2020, 9, 1),
        )
        Employee.objects.create(
            last_name='Козлов', first_name='Игорь', patronymic='Олегович',
            position='Заведующий', qualification='Высшая категория',
            education='Высшее педагогическое', experience_years=22,
            phone='+79993334455', hire_date=date(2010, 1, 15),
        )

        admin = User.objects.create_superuser(
            username='admin', password='admin12345', email='admin@example.org',
            role=User.Role.ADMIN,
        )
        admin.first_name = 'Администратор'
        admin.save()
        User.objects.create_user(
            username='head', password='head12345', role=User.Role.HEAD,
        )
        User.objects.create_user(
            username='teacher', password='teacher12345',
            role=User.Role.TEACHER, employee=teacher_emp,
        )

        children_data = [
            ('Иванов', 'Пётр', 'Сергеевич', date(2020, 5, 15), g1, 'I'),
            ('Смирнова', 'Мария', 'Петровна', date(2020, 8, 3), g1, 'II'),
            ('Кузнецов', 'Артём', 'Дмитриевич', date(2020, 1, 20), g1, 'I'),
            ('Попова', 'София', 'Александровна', date(2020, 11, 10), g1, 'I'),
            ('Васильев', 'Михаил', 'Андреевич', date(2018, 4, 5), g2, 'II'),
            ('Новикова', 'Анастасия', 'Игоревна', date(2018, 7, 22), g2, 'I'),
            ('Морозов', 'Илья', 'Романович', date(2018, 2, 14), g2, 'III'),
        ]
        children = []
        for last, first, patro, bdate, group, hg in children_data:
            children.append(
                Child.objects.create(
                    last_name=last, first_name=first, patronymic=patro,
                    birth_date=bdate, enrollment_date=date(2024, 9, 1),
                    group=group, health_group=hg, status='active',
                    medical_notes={'allergies': [], 'chronic': []},
                )
            )

        Parent.objects.create(
            last_name='Иванова', first_name='Ольга', patronymic='Викторовна',
            phone='+79995556677', relation='mother',
        ).children.add(children[0])

        today = date.today()
        for offset in range(7):
            day = today - timedelta(days=offset)
            for child in children:
                AttendanceRecord.objects.update_or_create(
                    child=child, date=day,
                    defaults={
                        'is_present': offset % 4 != 0,
                        'absence_reason': '' if offset % 4 != 0 else 'illness',
                    },
                )

        self.stdout.write(self.style.SUCCESS(
            'Демоданные созданы. Учётки: admin/admin12345, head/head12345, teacher/teacher12345.'
        ))
