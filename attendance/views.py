"""Представления приложения attendance.

Главное представление — mark_attendance — приведено в ВКР (раздел 3.1)
почти в исходном виде. Доработки по сравнению с фрагментом из ВКР:
1. Добавлена валидация selected_date_str (защита от некорректного ввода).
2. Воспитатель видит только свою группу (из ролевых требований).
3. Сохранение посещаемости вынесено в одну транзакцию.

Подробности — в DOCS/replacements.md.
"""

from datetime import date

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render

from accounts.permissions import role_required
from children.models import Child
from groups.models import Group

from .models import AttendanceRecord


def _parse_date(raw: str | None) -> date:
    if not raw:
        return date.today()
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return date.today()


@role_required('admin', 'head', 'teacher')
def mark_attendance(request):
    """Электронная форма ежедневной отметки посещаемости (ВКР, 3.1)."""
    user = request.user

    groups = Group.objects.order_by('name')
    if user.role == user.Role.TEACHER and user.employee_id:
        groups = groups.filter(staff_members=user.employee).distinct()

    selected_group_id = request.GET.get('group_id') or request.POST.get('group_id')
    selected_date_str = (
        request.GET.get('date') or request.POST.get('date') or str(date.today())
    )
    selected_date = _parse_date(selected_date_str)

    children_in_group: list[Child] = []
    if selected_group_id:
        # Воспитатель не может работать с чужой группой.
        if user.role == user.Role.TEACHER and not groups.filter(pk=selected_group_id).exists():
            messages.error(request, 'Эта группа вам недоступна.')
            return redirect('attendance:mark')

        children_in_group = list(
            Child.objects.filter(group_id=selected_group_id, status='active').order_by('last_name')
        )
        existing = {
            rec.child_id: rec
            for rec in AttendanceRecord.objects.filter(
                child__group_id=selected_group_id,
                date=selected_date,
            )
        }
        for child in children_in_group:
            child.existing_record = existing.get(child.id)

    if request.method == 'POST' and selected_group_id:
        with transaction.atomic():
            for child in Child.objects.filter(
                group_id=selected_group_id, status='active'
            ):
                is_present = request.POST.get(f'present_{child.id}') == 'on'
                reason = (
                    ''
                    if is_present
                    else request.POST.get(f'reason_{child.id}', '')
                )
                AttendanceRecord.objects.update_or_create(
                    child=child,
                    date=selected_date,
                    defaults={'is_present': is_present, 'absence_reason': reason},
                )
        messages.success(request, f'Посещаемость за {selected_date} сохранена.')
        return redirect(
            f'{request.path}?group_id={selected_group_id}&date={selected_date.isoformat()}'
        )

    return render(
        request,
        'attendance/mark.html',
        {
            'groups': groups,
            'children': children_in_group,
            'selected_group_id': int(selected_group_id) if selected_group_id else None,
            'selected_date': selected_date.isoformat(),
            'absence_reasons': AttendanceRecord.ABSENCE_REASONS,
        },
    )
