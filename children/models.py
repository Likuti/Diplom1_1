"""Модели воспитанника и родителя.

Реализованы по диплому (раздел 2.3, таблицы children_child / children_parent /
children_parentchild). Контроль наполняемости группы реализован через clean().
"""

from django.core.exceptions import ValidationError
from django.db import models

from groups.models import Group


class Child(models.Model):
    HEALTH_GROUPS = [
        ('I', 'I группа'),
        ('II', 'II группа'),
        ('III', 'III группа'),
        ('IV', 'IV группа'),
        ('V', 'V группа'),
    ]
    STATUS_CHOICES = [
        ('active', 'Посещает'),
        ('expelled', 'Отчислен'),
        ('graduated', 'Выпущен'),
    ]

    last_name = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True, default='')
    birth_date = models.DateField('Дата рождения')
    enrollment_date = models.DateField('Дата зачисления')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Группа',
    )
    health_group = models.CharField(
        'Группа здоровья',
        max_length=5,
        choices=HEALTH_GROUPS,
        default='I',
    )
    medical_notes = models.JSONField(
        'Медицинские сведения',
        default=dict,
        blank=True,
        help_text='Например: {"allergies": ["пыльца"], "chronic": []}',
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Воспитанник'
        verbose_name_plural = 'Воспитанники'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['group']),
            models.Index(fields=['status']),
            models.Index(fields=['last_name']),
        ]

    def full_name(self) -> str:
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(parts)

    def __str__(self) -> str:
        return self.full_name()

    def clean(self) -> None:
        """Контроль предельной наполняемости группы.

        Диплом, функциональное требование 2: «Система должна автоматически
        контролировать соблюдение предельной наполняемости и выдавать
        предупреждение при попытке зачисления сверх нормы».
        """
        super().clean()
        if self.group_id and self.status == 'active':
            qs = Child.objects.filter(group_id=self.group_id, status='active')
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.count() >= self.group.max_capacity:
                raise ValidationError({
                    'group': (
                        f'В группе «{self.group.name}» нет свободных мест '
                        f'(заполнено {qs.count()} из {self.group.max_capacity}).'
                    ),
                })


class Parent(models.Model):
    RELATION_CHOICES = [
        ('mother', 'Мать'),
        ('father', 'Отец'),
        ('guardian', 'Опекун'),
        ('other', 'Иное'),
    ]

    last_name = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True, default='')
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Электронная почта', blank=True, default='')
    address = models.TextField('Адрес', blank=True, default='')
    relation = models.CharField('Степень родства', max_length=20, choices=RELATION_CHOICES)
    children = models.ManyToManyField(
        Child,
        related_name='parents',
        verbose_name='Дети',
        blank=True,
    )

    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'
        ordering = ['last_name', 'first_name']

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name} ({self.get_relation_display()})'
