from django.urls import path
from .views import register_parent, ParentChildListView



urlpatterns = [
    path('register/', register_parent, name="register-parent"),
    path('childs', ParentChildListView.as_view(), name="parent-child-list")
]
