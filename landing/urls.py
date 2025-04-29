from django.urls import path
from .views import home, signin
from . import views
from django.contrib.auth import views as auth_views
from .views import monitoring_calendar
from .views import csc_page
from .views import dashboard
from .views import application_request
from .views import employees_profile
from .views import history
from .views import fold
from .views import settings

app_name = 'landing'

urlpatterns = [
    path('', home, name='home'),
    path('signin/', signin, name='signin'), 
    path("signup/", views.signup_view, name="signup"),
    path('login/', views.login_view, name='login'),
    path('monitoring_calendar/',monitoring_calendar, name='monitoring_calendar'),
    path('csc_page/',csc_page, name='csc_page'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('application_request/', application_request, name = 'application_request'),
    path('history/', history, name = 'history'),
    path('employees_profile/', employees_profile, name = 'employees_profile'),
    path('fold/', fold, name = 'fold'),
    path('settings/', settings, name = 'settings'),


]
