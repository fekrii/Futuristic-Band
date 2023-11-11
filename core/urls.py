from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from django.conf import settings

schema_view = get_swagger_view(title='Futuristic Band swagger')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('_auth.urls')),
    path('parent/', include('parent.urls')),
    path('child/', include('child.urls')),
    path('school/', include('school.urls')),
    path('docs/', schema_view),

    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)