"""URL configuration for kindergarten_project."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('groups/', include('groups.urls', namespace='groups')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('', RedirectView.as_view(pattern_name='reports:dashboard', permanent=False)),
]

admin.site.site_header = 'Информационная система детского сада'
admin.site.site_title = 'ИС детского сада'
admin.site.index_title = 'Администрирование'
