from django.contrib import admin
from django.urls import path
from landing import views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('landing/', views.landing_page, name='landing_page'),
    path('monitoring_calendar/', views.monitoring_calendar, name='monitoring_calendar'),
    path('csc_page/', views.csc_page, name='csc_page'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('employees_profile/', views.employees_profile, name = 'employees_profile'),
    path('history/', views.history, name = 'history'),
    path('fold/', views.fold, name = 'fold'),
    path('settings/', views.settings, name = 'settings'),
    path('fold/<str:folder_name>/', views.folder_detail, name='folder_detail'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('application_request/', views.application_request, name = 'application_request'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
