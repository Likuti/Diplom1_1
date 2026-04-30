"""Тесты приложения groups."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from children.models import Child
from staff.models import Employee

from .models import Group

User = get_user_model()


class GroupModelTest(TestCase):
    def test_current_count_excludes_expelled(self):
        g = Group.objects.create(
            name='Г', age_category='3-4 года',
            direction='общеразвивающая', max_capacity=5,
        )
        Child.objects.create(
            last_name='А', first_name='А',
            birth_date=date(2019, 1, 1), enrollment_date=date(2024, 9, 1),
            group=g, health_group='I', status='active',
        )
        Child.objects.create(
            last_name='Б', first_name='Б',
            birth_date=date(2019, 1, 1), enrollment_date=date(2024, 9, 1),
            group=g, health_group='I', status='expelled',
        )
        self.assertEqual(g.current_count, 1)
        self.assertTrue(g.has_free_places)


class GroupViewsTest(TestCase):
    def setUp(self):
        self.g1 = Group.objects.create(
            name='Г1', age_category='3-4 года',
            direction='общеразвивающая', max_capacity=10,
        )
        self.g2 = Group.objects.create(
            name='Г2', age_category='4-5 лет',
            direction='общеразвивающая', max_capacity=10,
        )
        self.emp = Employee.objects.create(
            last_name='П', first_name='А', position='Воспитатель',
            hire_date=date(2020, 1, 1), group=self.g1,
        )
        self.teacher = User.objects.create_user(
            username='t', password='p', role='teacher', employee=self.emp,
        )

    def test_teacher_sees_only_own_group(self):
        self.client.login(username='t', password='p')
        r = self.client.get(reverse('groups:list'))
        self.assertEqual(r.status_code, 200)
        groups = list(r.context['groups'])
        self.assertEqual(groups, [self.g1])

    def test_teacher_forbidden_on_foreign_group_detail(self):
        self.client.login(username='t', password='p')
        r = self.client.get(reverse('groups:detail', args=[self.g2.pk]))
        self.assertEqual(r.status_code, 403)
