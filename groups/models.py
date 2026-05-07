"""Модель группы детского сада.

Соответствует таблице groups_group из ВКР (раздел 2.3).
"""

from django.db import models


class Group(models.Model):
    class AgeCategory(models.TextChoices):
        NURSERY = '1-2 года', '1-2 года (ясельная)'
        FIRST_YOUNGER = '2-3 года', '2-3 года (первая младшая)'
        SECOND_YOUNGER = '3-4 года', '3-4 года (вторая младшая)'
        MIDDLE = '4-5 лет', '4-5 лет (средняя)'
        SENIOR = '5-6 лет', '5-6 лет (старшая)'
        PREPARATORY = '6-7 лет', '6-7 лет (подготовительная)'

    class Direction(models.TextChoices):
        GENERAL = 'общеразвивающая', 'Общеразвивающая'
        COMPENSATING = 'компенсирующая', 'Компенсирующая'
        COMBINED = 'комбинированная', 'Комбинированная'

    name = models.CharField('Название', max_length=100, unique=True)
    age_category = models.CharField(
        'Возрастная категория',
        max_length=50,
        choices=AgeCategory.choices,
    )
    direction = models.CharField(
        'Направленность',
        max_length=50,
        choices=Direction.choices,
        default=Direction.GENERAL,
    )
    max_capacity = models.PositiveSmallIntegerField('Максимальная наполняемость', default=25)
    description = models.TextField('Описание', blank=True, default='')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    @property
    def current_count(self) -> int:
        """Сколько активных воспитанников сейчас закреплено за группой."""
        return self.children.filter(status='active').count()

    @property
    def has_free_places(self) -> bool:
        return self.current_count < self.max_capacity
