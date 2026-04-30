from django.contrib import admin

from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'age_category', 'direction', 'max_capacity', 'current_count')
    list_filter = ('age_category', 'direction')
    search_fields = ('name',)

    @admin.display(description='Сейчас в группе')
    def current_count(self, obj: Group) -> int:
        return obj.current_count
