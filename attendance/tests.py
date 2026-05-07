"""Тесты приложения attendance.

Базовый набор тестов взят из диплома (раздел 3.2). Добавлены:
- проверка update_or_create через POST формы;
- проверка ролевого доступа (воспитатель не видит чужую группу).
"""

from datetime import date

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from children.models import Child
from groups.models import Group
from staff.models import Employee

from .models import AttendanceRecord

User = get_user_model()


class AttendanceModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(
            name='Ромашка',
            age_category='3-4 года',
            direction='общеразвивающая',
            max_capacity=25,
        )
        self.child = Child.objects.create(
            last_name='Иванов',
            first_name='Пётр',
            birth_date=date(2020, 5, 15),
            enrollment_date=date(2023, 9, 1),
            group=self.group,
            health_group='I',
        )

    def test_create_attendance_record(self):
        record = AttendanceRecord.objects.create(
            child=self.child, date=date(2025, 4, 10), is_present=True
        )
        self.assertTrue(record.is_present)
        self.assertEqual(record.absence_reason, '')

    def test_unique_constraint(self):
        AttendanceRecord.objects.create(
            child=self.child, date=date(2025, 4, 10), is_present=True
        )
        with self.assertRaises(IntegrityError):
            AttendanceRecord.objects.create(
                child=self.child, date=date(2025, 4, 10), is_present=False
            )

    def test_absence_with_reason(self):
        record = AttendanceRecord.objects.create(
            child=self.child,
            date=date(2025, 4, 11),
            is_present=False,
            absence_reason='illness',
        )
        self.assertFalse(record.is_present)
        self.assertEqual(record.absence_reason, 'illness')


class AttendanceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.group = Group.objects.create(
            name='Ромашка',
            age_category='3-4 года',
            direction='общеразвивающая',
            max_capacity=25,
        )
        self.other_group = Group.objects.create(
            name='Звёздочка',
            age_category='4-5 лет',
            direction='общеразвивающая',
            max_capacity=25,
        )
        self.employee = Employee.objects.create(
            last_name='Петрова',
            first_name='Анна',
            position='Воспитатель',
            hire_date=date(2020, 1, 1),
            group=self.group,
        )
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role=User.Role.TEACHER,
            employee=self.employee,
        )
        self.head = User.objects.create_user(
            username='head1',
            password='testpass123',
            role=User.Role.HEAD,
        )
        self.child = Child.objects.create(
            last_name='Иванов',
            first_name='Пётр',
            birth_date=date(2020, 5, 15),
            enrollment_date=date(2023, 9, 1),
            group=self.group,
            health_group='I',
        )

    def test_mark_attendance_requires_login(self):
        response = self.client.get(reverse('attendance:mark'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_mark_attendance_authenticated(self):
        self.client.login(username='teacher1', password='testpass123')
        response = self.client.get(reverse('attendance:mark'))
        self.assertEqual(response.status_code, 200)

    def test_post_creates_records(self):
        self.client.login(username='head1', password='testpass123')
        response = self.client.post(
            reverse('attendance:mark'),
            data={
                'group_id': self.group.id,
                'date': '2025-04-15',
                f'present_{self.child.id}': 'on',
            },
        )
        self.assertEqual(response.status_code, 302)
        rec = AttendanceRecord.objects.get(child=self.child, date=date(2025, 4, 15))
        self.assertTrue(rec.is_present)

    def test_post_updates_existing(self):
        AttendanceRecord.objects.create(
            child=self.child, date=date(2025, 4, 16), is_present=True
        )
        self.client.login(username='head1', password='testpass123')
        self.client.post(
            reverse('attendance:mark'),
            data={
                'group_id': self.group.id,
                'date': '2025-04-16',
                f'reason_{self.child.id}': 'illness',
            },
        )
        rec = AttendanceRecord.objects.get(child=self.child, date=date(2025, 4, 16))
        self.assertFalse(rec.is_present)
        self.assertEqual(rec.absence_reason, 'illness')

    def test_teacher_cannot_access_foreign_group(self):
        self.client.login(username='teacher1', password='testpass123')
        response = self.client.get(
            reverse('attendance:mark'),
            data={'group_id': self.other_group.id, 'date': '2025-04-17'},
        )
        # Должен быть редирект с flash-сообщением.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('attendance:mark'))
