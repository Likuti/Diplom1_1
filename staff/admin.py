from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'group', 'hire_date', 'is_active')
    list_filter = ('position', 'is_active', 'group', 'qualification')
    search_fields = ('last_name', 'first_name', 'phone', 'email')
    date_hierarchy = 'hire_date'
