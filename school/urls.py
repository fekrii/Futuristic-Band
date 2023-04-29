from django.urls import path
from .views import register_school, SchoolView, HomeView



urlpatterns = [
    path('', SchoolView.as_view(), name="school-view"),
    path('register/', register_school),
    path('home/', HomeView.as_view(), name="home-view")
]
