"""Декораторы и утилиты ролевой авторизации."""

from functools import wraps
from typing import Iterable

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles: Iterable[str]):
    """Допускает только пользователей с указанными ролями (или суперпользователей).

    Используется так:
        @role_required('admin', 'head')
        def view(request): ...
    """

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied('Недостаточно прав для доступа к этой странице.')

        return _wrapped

    return decorator
