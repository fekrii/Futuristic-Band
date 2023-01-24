from django.urls import path
from .views import register_school



urlpatterns = [
    path('register/', register_school),
]
