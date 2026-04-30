from django.contrib.auth.forms import AuthenticationForm
from django import forms


class StyledLoginForm(AuthenticationForm):
    """Стандартная форма входа с bootstrap-классами."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
        self.fields['username'].widget.attrs['placeholder'] = 'Логин'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'

    error_messages = {
        'invalid_login': 'Неверный логин или пароль.',
        'inactive': 'Учётная запись отключена.',
    }
