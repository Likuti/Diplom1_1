from django.contrib import admin

from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('child', 'date', 'is_present', 'absence_reason')
    list_filter = ('is_present', 'absence_reason', 'date', 'child__group')
    search_fields = ('child__last_name', 'child__first_name')
    date_hierarchy = 'date'
    autocomplete_fields = ('child',)
