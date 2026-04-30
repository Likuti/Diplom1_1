"""Тесты приложения children."""

from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from groups.models import Group

from .models import Child, Parent


class ChildModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(
            name='Солнышко',
            age_category='5-6 лет',
            direction='общеразвивающая',
            max_capacity=2,
        )

    def _make_child(self, last_name: str = 'Сидоров') -> Child:
        return Child.objects.create(
            last_name=last_name,
            first_name='Иван',
            birth_date=date(2019, 6, 1),
            enrollment_date=date(2024, 9, 1),
            group=self.group,
            health_group='II',
        )

    def test_full_name_with_patronymic(self):
        c = self._make_child()
        c.patronymic = 'Иванович'
        self.assertEqual(c.full_name(), 'Сидоров Иван Иванович')

    def test_full_name_without_patronymic(self):
        self.assertEqual(self._make_child().full_name(), 'Сидоров Иван')

    def test_capacity_overflow_raises(self):
        self._make_child('А')
        self._make_child('Б')
        third = Child(
            last_name='В',
            first_name='Иван',
            birth_date=date(2019, 6, 1),
            enrollment_date=date(2024, 9, 1),
            group=self.group,
            health_group='I',
            status='active',
        )
        with self.assertRaises(ValidationError):
            third.full_clean()

    def test_medical_notes_default_dict(self):
        c = self._make_child()
        self.assertEqual(c.medical_notes, {})


class ParentModelTest(TestCase):
    def test_m2m_with_children(self):
        group = Group.objects.create(
            name='Берёзка',
            age_category='4-5 лет',
            direction='общеразвивающая',
            max_capacity=10,
        )
        child = Child.objects.create(
            last_name='Алексеев',
            first_name='Олег',
            birth_date=date(2019, 1, 1),
            enrollment_date=date(2024, 9, 1),
            group=group,
            health_group='I',
        )
        parent = Parent.objects.create(
            last_name='Алексеева',
            first_name='Мария',
            phone='+79991234567',
            relation='mother',
        )
        parent.children.add(child)
        self.assertIn(parent, child.parents.all())
        self.assertEqual(str(parent), 'Алексеева Мария (Мать)')
