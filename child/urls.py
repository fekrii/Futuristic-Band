from django.urls import path
from .views import register_child, ChildWalletView, ChildView, BannedFoodView, ChildDaysOffView



urlpatterns = [
    path('register/', register_child, name="register-child"),
    path('<int:child_id>', ChildView.as_view(), name="child-view"),
    path('<int:child_id>/wallet', ChildWalletView.as_view(), name="child-wallet-view"),
    path('<int:child_id>/banned-food', BannedFoodView.as_view(), name="child-banned-food-view"),
    path('<int:child_id>/days-off', ChildDaysOffView.as_view(), name="child-days-off-view"),
    
]
