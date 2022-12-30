from django.urls import path
from .views import register_parent



urlpatterns = [
    path('register/', register_parent),
]
