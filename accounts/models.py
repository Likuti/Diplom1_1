"""Кастомная модель пользователя с ролевой моделью доступа.

В системе три роли: Администратор / Заведующий / Воспитатель. Расширяем
AbstractUser, чтобы воспользоваться готовой инфраструктурой Django Auth
(хеширование пароля, сессии, проверка авторизации) и при этом добавить поле
role и связь с employee.
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
