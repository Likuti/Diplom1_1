"""Тесты приложения reports."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from attendance.models import AttendanceRecord
from children.models import Child
from groups.models import Group
from staff.models import Employee

User = get_user_model()


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.head = User.objects.create_user(
            username='head1', password='pass', role=User.Role.HEAD
        )
        self.group = Group.objects.create(
            name='Г1', age_category='3-4 года', direction='общеразвивающая', max_capacity=10
        )
        self.child = Child.objects.create(
            last_name='Иванов', first_name='Пётр',
            birth_date=date(2020, 1, 1), enrollment_date=date(2024, 9, 1),
            group=self.group, health_group='I',
        )

    def test_dashboard_requires_login(self):
        r = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(r.status_code, 302)

    def test_dashboard_renders(self):
        self.client.login(username='head1', password='pass')
        r = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Сводка')
        self.assertContains(r, '1')  # один активный ребёнок

    def test_dashboard_attendance_pct(self):
        AttendanceRecord.objects.create(child=self.child, date=date.today(), is_present=True)
        self.client.login(username='head1', password='pass')
        r = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(r.context['month_attendance_pct'], 100)


class StaffReportTest(TestCase):
    def test_teacher_cannot_open_staff_report(self):
        teacher = User.objects.create_user(
            username='t1', password='pass', role=User.Role.TEACHER
        )
        self.client.login(username='t1', password='pass')
        r = self.client.get(reverse('reports:staff'))
        self.assertEqual(r.status_code, 403)

    def test_high_qualification_count_handles_cyrillic_case(self):
        """Регрессия: SQLite icontains не сворачивает регистр для кириллицы."""
        head = User.objects.create_user(
            username='h1', password='pass', role=User.Role.HEAD
        )
        Employee.objects.create(
            last_name='А', first_name='А', position='Воспитатель',
            qualification='Высшая категория', hire_date=date(2020, 1, 1),
        )
        Employee.objects.create(
            last_name='Б', first_name='Б', position='Воспитатель',
            qualification='высшая категория', hire_date=date(2020, 1, 1),
        )
        Employee.objects.create(
            last_name='В', first_name='В', position='Воспитатель',
            qualification='Первая категория', hire_date=date(2020, 1, 1),
        )
        self.client.login(username='h1', password='pass')
        r = self.client.get(reverse('reports:staff'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['high_qual'], 2)
        self.assertEqual(r.context['total'], 3)
