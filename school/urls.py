from django.urls import path
from .views import register_school, SchoolView



urlpatterns = [
    path('', SchoolView.as_view(), name="school-view"),
    path('register/', register_school),
]
