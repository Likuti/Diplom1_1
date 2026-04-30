"""Представления приложения reports.

dashboard — взят из курсовой (раздел 3.1) с минимальными доработками.
Дополнительно реализованы:
- attendance_report: сводный отчёт по посещаемости группы за период,
- groups_report: отчёт по наполняемости всех групп,
- staff_report: отчёт по кадровому составу,
- contingent_report: отчёт по движению контингента.
Все отчёты — из функционального требования 5 («Подсистема отчётности»).
"""

from collections import Counter
from datetime import date, timedelta

from django.db.models import Avg, Count, Q
from django.shortcuts import render

from accounts.permissions import role_required
from attendance.models import AttendanceRecord
from children.models import Child
from groups.models import Group
from staff.models import Employee


def _parse_date(raw: str | None, default: date) -> date:
    if not raw:
        return default
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return default


@role_required('admin', 'head', 'teacher')
def dashboard(request):
    """Главная страница после входа: сводка по учреждению (курсовая, 3.1)."""
    total_active_children = Child.objects.filter(status='active').count()
    total_employees = Employee.objects.filter(is_active=True).count()
    total_groups = Group.objects.count()

    group_stats = list(
        Group.objects.annotate(
            current_count=Count('children', filter=Q(children__status='active'))
        ).values('id', 'name', 'max_capacity', 'current_count')
    )
    for g in group_stats:
        g['occupancy_pct'] = (
            round(g['current_count'] / g['max_capacity'] * 100)
            if g['max_capacity']
            else 0
        )

    today = date.today()
    first_day = today.replace(day=1)
    month_records = AttendanceRecord.objects.filter(
        date__gte=first_day, date__lte=today
    )
    total_records = month_records.count()
    present_records = month_records.filter(is_present=True).count()
    month_attendance_pct = (
        round(present_records / total_records * 100) if total_records else 0
    )

    return render(
        request,
        'reports/dashboard.html',
        {
            'total_active_children': total_active_children,
            'total_employees': total_employees,
            'total_groups': total_groups,
            'group_stats': group_stats,
            'month_attendance_pct': month_attendance_pct,
            'period_label': f'{first_day.isoformat()} — {today.isoformat()}',
        },
    )


@role_required('admin', 'head')
def attendance_report(request):
    """Сводный отчёт по посещаемости группы за период."""
    today = date.today()
    period_from = _parse_date(request.GET.get('from'), today.replace(day=1))
    period_to = _parse_date(request.GET.get('to'), today)
    group_id = request.GET.get('group_id')

    groups = Group.objects.order_by('name')
    rows: list[dict] = []
    summary_pct = None

    if group_id:
        records = AttendanceRecord.objects.filter(
            child__group_id=group_id,
            date__gte=period_from,
            date__lte=period_to,
        )
        per_child = (
            records.values('child_id', 'child__last_name', 'child__first_name')
            .annotate(
                total=Count('id'),
                present=Count('id', filter=Q(is_present=True)),
            )
            .order_by('child__last_name')
        )
        for row in per_child:
            pct = round(row['present'] / row['total'] * 100) if row['total'] else 0
            rows.append(
                {
                    'child': f"{row['child__last_name']} {row['child__first_name']}",
                    'present': row['present'],
                    'total': row['total'],
                    'pct': pct,
                }
            )
        total = records.count()
        present = records.filter(is_present=True).count()
        summary_pct = round(present / total * 100) if total else 0

    return render(
        request,
        'reports/attendance.html',
        {
            'groups': groups,
            'rows': rows,
            'summary_pct': summary_pct,
            'period_from': period_from.isoformat(),
            'period_to': period_to.isoformat(),
            'selected_group_id': int(group_id) if group_id else None,
        },
    )


@role_required('admin', 'head')
def groups_report(request):
    """Отчёт по наполняемости всех групп."""
    rows = list(
        Group.objects.annotate(
            current_count=Count('children', filter=Q(children__status='active'))
        )
        .values('name', 'age_category', 'direction', 'max_capacity', 'current_count')
        .order_by('name')
    )
    for r in rows:
        r['free'] = max(r['max_capacity'] - r['current_count'], 0)
        r['occupancy_pct'] = (
            round(r['current_count'] / r['max_capacity'] * 100)
            if r['max_capacity']
            else 0
        )
    return render(request, 'reports/groups.html', {'rows': rows})


@role_required('admin', 'head')
def staff_report(request):
    """Отчёт по кадровому составу."""
    qs = Employee.objects.filter(is_active=True)
    by_position = Counter(qs.values_list('position', flat=True))
    avg_experience = qs.aggregate(v=Avg('experience_years'))['v'] or 0
    high_qual = qs.filter(qualification__icontains='высш').count()
    total = qs.count()
    return render(
        request,
        'reports/staff.html',
        {
            'total': total,
            'avg_experience': round(avg_experience, 1) if avg_experience else 0,
            'high_qual': high_qual,
            'high_qual_pct': round(high_qual / total * 100) if total else 0,
            'by_position': sorted(by_position.items(), key=lambda x: -x[1]),
        },
    )


@role_required('admin', 'head')
def contingent_report(request):
    """Отчёт по движению контингента за период."""
    today = date.today()
    default_from = today - timedelta(days=30)
    period_from = _parse_date(request.GET.get('from'), default_from)
    period_to = _parse_date(request.GET.get('to'), today)

    enrolled = Child.objects.filter(
        enrollment_date__gte=period_from, enrollment_date__lte=period_to
    ).count()
    expelled = Child.objects.filter(
        status='expelled',
        updated_at__date__gte=period_from,
        updated_at__date__lte=period_to,
    ).count()
    graduated = Child.objects.filter(
        status='graduated',
        updated_at__date__gte=period_from,
        updated_at__date__lte=period_to,
    ).count()

    return render(
        request,
        'reports/contingent.html',
        {
            'enrolled': enrolled,
            'expelled': expelled,
            'graduated': graduated,
            'period_from': period_from.isoformat(),
            'period_to': period_to.isoformat(),
        },
    )
