"""Модель сотрудника детского сада.

Отображается в таблицу staff_employee. Содержит ФИО, должность, образование,
квалификационную категорию, контакты и связь с закреплёнными группами
(M2M поле groups).
"""

from django.db import models

from groups.models import Group


class Employee(models.Model):
    last_name = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True, default='')

    position = models.CharField('Должность', max_length=100)
    qualification = models.CharField('Квалификационная категория', max_length=100, blank=True, default='')
    education = models.CharField('Образование', max_length=200, blank=True, default='')
    experience_years = models.PositiveSmallIntegerField('Стаж (лет)', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, default='')
    email = models.EmailField('Электронная почта', blank=True, default='')

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_members',
        verbose_name='Группа',
    )
    hire_date = models.DateField('Дата приёма')
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name']

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self) -> str:
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(parts)
