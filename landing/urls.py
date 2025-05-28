from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.landing_page, name='landing_page'),

    path('signup/', views.signup, name='signup'),

    # Use Django's built-in login view with your custom template
    path('login/', auth_views.LoginView.as_view(template_name='landing/login.html'), name='login'),

    path('landing_page/', views.landing_page, name='landing_page'),

    path('monitoring_calendar/', views.monitoring_calendar, name='monitoring_calendar'),
    path('csc_page/', views.csc_page, name='csc_page'),

#DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('application_request/', views.application_request, name='application_request'),

    path('history/', views.history, name='history'),

#EMPLOYEES PROFILE
    path('employees_profile/', views.employees_profile, name='employees_profile'),
    path('api/employees/', views.get_employees, name='get_employees'),
    path('api/employees/add/', views.add_employee, name='add_employee'),
    path('api/employees/update/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('api/employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),

#file categorization
    path('folders/', views.fold, name='fold'),
    path('folders/<str:folder_name>/', views.folder_detail, name='folder_detail'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('settings/', views.settings, name='settings'),
    path('delete-folder/', views.delete_folder, name='delete_folder'),


    
#monitoring_barangay
    path('monitoring/barangay/<int:barangay_id>/', views.barangay_detail, name='barangay_detail'),


#application letter
     path('document/<str:application_id>/<str:doc_type>/', views.serve_document, name='serve_document'),
    path('view-document/<str:application_id>/<str:doc_type>/', views.view_document_online, name='view_document_online'),
]
