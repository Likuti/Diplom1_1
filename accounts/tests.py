"""Тесты приложения accounts."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserRoleTest(TestCase):
    def test_role_properties(self):
        u = User.objects.create_user(username='u', password='p', role='head')
        self.assertTrue(u.is_head)
        self.assertFalse(u.is_teacher)
        self.assertFalse(u.is_kindergarten_admin)

    def test_default_role_is_teacher(self):
        u = User.objects.create_user(username='u', password='p')
        self.assertTrue(u.is_teacher)

    def test_superuser_is_admin(self):
        u = User.objects.create_superuser(username='su', password='p')
        self.assertTrue(u.is_kindergarten_admin)


class LoginViewTest(TestCase):
    def test_login_page_renders(self):
        r = self.client.get(reverse('accounts:login'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Вход')

    def test_invalid_login(self):
        r = self.client.post(
            reverse('accounts:login'),
            {'username': 'nobody', 'password': 'wrong'},
        )
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Неверный')

    def test_valid_login_redirects_to_dashboard(self):
        User.objects.create_user(username='u', password='p', role='head')
        r = self.client.post(
            reverse('accounts:login'),
            {'username': 'u', 'password': 'p'},
        )
        self.assertEqual(r.status_code, 302)
