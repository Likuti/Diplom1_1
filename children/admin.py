from django.contrib import admin

from .models import Child, Parent


class ParentInline(admin.TabularInline):
    """Связь родитель-ребёнок прямо из карточки воспитанника."""

    model = Parent.children.through
    extra = 1
    verbose_name = 'Родитель'
    verbose_name_plural = 'Родители'


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date', 'group', 'health_group', 'status')
    list_filter = ('status', 'group', 'health_group')
    search_fields = ('last_name', 'first_name')
    date_hierarchy = 'enrollment_date'
    inlines = [ParentInline]
    autocomplete_fields = ('group',)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone', 'relation')
    search_fields = ('last_name', 'first_name', 'phone')
    list_filter = ('relation',)
    filter_horizontal = ('children',)
