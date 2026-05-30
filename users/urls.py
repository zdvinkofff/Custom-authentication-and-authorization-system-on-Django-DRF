from django.urls import path
from users.views import (
    RegisterView,
    LoginView,
    ProfileView,
    LogoutView,
    AdminPanelView,
    DeleteAccountView
)

urlpatterns = [
    path(
        'register/',
        RegisterView.as_view()
    ),

    path(
        'login/',
        LoginView.as_view()
    ),

    path(
        'profile/',
        ProfileView.as_view()
    ),

    path(
        'logout/',
        LogoutView.as_view()
    ),
    path(
        'admin-panel/',
        AdminPanelView.as_view()
    ),
    path(
        'delete-account/',
        DeleteAccountView.as_view()
    ),
]