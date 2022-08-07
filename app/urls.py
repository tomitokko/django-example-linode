from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('new-order', views.new_order, name='new-order'),
    path('history', views.history, name='history'),
    path('project-form', views.project_form, name='project-form'),
    path('project-notification', views.project_notification, name='project-notification'),
    path('alert-success', views.alert_success, name='alert-success'),
    path('current-alerts', views.current_alerts, name='current-alerts'),
    path('delete-alert', views.delete_alert, name='delete-alert'),
    path('send-alert', views.send_alert, name='send-alert'),
    # path('test-alert', views.test_alert, name='test-alert'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]