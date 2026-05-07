"""Кастомная модель пользователя с ролевой моделью доступа.

Диплом описывает три роли: Администратор / Заведующий / Воспитатель.
Реализуется через расширение AbstractUser (см. дипломная, раздел 2.3 — таблица
accounts_user, комментарий «Для аутентификации используется встроенная система
Django Auth с расширением через кастомную модель пользователя (AbstractUser)»).
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь системы с ролью."""

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        HEAD = 'head', 'Заведующий'
        TEACHER = 'teacher', 'Воспитатель'

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=Role.choices,
        default=Role.TEACHER,
    )
    employee = models.OneToOneField(
        'staff.Employee',
        verbose_name='Сотрудник',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_teacher(self) -> bool:
        return self.role == self.Role.TEACHER

    @property
    def is_head(self) -> bool:
        return self.role == self.Role.HEAD

    @property
    def is_kindergarten_admin(self) -> bool:
        return self.role == self.Role.ADMIN or self.is_superuser
