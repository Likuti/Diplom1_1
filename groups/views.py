from django.shortcuts import get_object_or_404, render

from accounts.permissions import role_required

from .models import Group


@role_required('admin', 'head', 'teacher')
def group_list(request):
    """Список всех групп. Воспитатель видит только свою группу."""
    user = request.user
    groups = Group.objects.all()
    if user.role == user.Role.TEACHER and user.employee_id:
        groups = groups.filter(staff_members=user.employee)
    return render(request, 'groups/group_list.html', {'groups': groups})


@role_required('admin', 'head', 'teacher')
def group_detail(request, pk: int):
    """Карточка группы со списком детей."""
    group = get_object_or_404(Group, pk=pk)
    user = request.user
    if user.role == user.Role.TEACHER:
        if not user.employee_id or group.staff_members.filter(pk=user.employee_id).count() == 0:
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied('Вы можете просматривать только свою группу.')
    return render(
        request,
        'groups/group_detail.html',
        {
            'group': group,
            'children_active': group.children.filter(status='active').order_by('last_name'),
            'employees': group.staff_members.filter(is_active=True),
        },
    )
