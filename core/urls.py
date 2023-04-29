from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('_auth.urls')),
    path('parent/', include('parent.urls')),
    path('child/', include('child.urls')),
    path('school/', include('school.urls')),
    
    
]
