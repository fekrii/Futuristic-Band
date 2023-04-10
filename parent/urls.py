from django.urls import path
from .views import register_parent, ParentChildListView, ParentListView, ParentView



urlpatterns = [
    path('', ParentListView.as_view(), name='all-parents'),
    path('<int:parent_id>', ParentView.as_view(), name="parent-view"),
    path('register/', register_parent, name="register-parent"),
    path('childs', ParentChildListView.as_view(), name="parent-child-list")
]
