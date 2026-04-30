from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance_report, name='attendance'),
    path('groups/', views.groups_report, name='groups'),
    path('staff/', views.staff_report, name='staff'),
    path('contingent/', views.contingent_report, name='contingent'),
]
