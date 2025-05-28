from django.contrib import admin
from django.urls import path, include
from landing import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

# All landing app urls including login inside here:
    path('', include('landing.urls', namespace='landing')),

#categorization
    path('folders/', views.fold, name='fold'),
    path('folders/<str:folder_name>/', views.folder_detail, name='folder_detail'), 
    path('folders/', include('landing.urls')),  # or whatever prefix you use# <-- Make sure this line exists


  

    # other urls like signup can also be inside landing.urls
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
