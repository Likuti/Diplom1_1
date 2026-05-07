"""Модель записи посещаемости воспитанника.

Таблица attendance_record. Одна строка — одна отметка на ребёнка в
конкретный день. На пару (child_id, date) наложено UNIQUE-ограничение,
чтобы исключить двойные отметки; форма использует update_or_create
для идемпотентного сохранения.
"""

from django.db import models

from children.models import Child


class AttendanceRecord(models.Model):
    ABSENCE_REASONS = [
        ('illness', 'Болезнь'),
        ('family', 'Семейные обстоятельства'),
        ('vacation', 'Отпуск родителей'),
        ('other', 'Иное'),
    ]

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='Воспитанник',
    )
    date = models.DateField('Дата')
    is_present = models.BooleanField('Присутствовал', default=True)
    absence_reason = models.CharField(
        'Причина отсутствия',
        max_length=20,
        choices=ABSENCE_REASONS,
        blank=True,
        default='',
    )

    class Meta:
        verbose_name = 'Запись посещаемости'
        verbose_name_plural = 'Записи посещаемости'
        constraints = [
            models.UniqueConstraint(fields=['child', 'date'], name='unique_child_date'),
        ]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['child', 'date']),
        ]
        ordering = ['-date', 'child__last_name']

    def __str__(self) -> str:
        status = 'присутствовал' if self.is_present else 'отсутствовал'
        return f'{self.child} — {self.date} — {status}'
