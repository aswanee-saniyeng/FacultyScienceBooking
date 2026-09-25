from django.urls import path
from .views import (
    login_view,
    register_view,
    logout_view,
    manage_users,
    edit_user,
    toggle_user_active,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('manage/', manage_users, name='manage_users'),
    path('manage/<int:user_id>/edit/', edit_user, name='edit_user'),
    path('manage/<int:user_id>/toggle/', toggle_user_active, name='toggle_user_active'),
]