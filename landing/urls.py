from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.signup, name='signup'),

    # Use Django's built-in login view with your custom template
    path('login/', auth_views.LoginView.as_view(template_name='landing/login.html'), name='login'),

    path('landing_page/', views.landing_page, name='landing_page'),

    path('monitoring_calendar/', views.monitoring_calendar, name='monitoring_calendar'),

    path('csc_page/', views.csc_page, name='csc_page'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('application_request/', views.application_request, name='application_request'),

    path('history/', views.history, name='history'),

    path('employees_profile/', views.employees_profile, name='employees_profile'),

    path('folders/', views.fold, name='fold'),

    path('folders/<str:folder_name>/', views.folder_detail, name='folder_detail'),

    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),

    path('settings/', views.settings, name='settings'),
]
