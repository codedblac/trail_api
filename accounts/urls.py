from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    UserListView,
    LogoutView,
    CustomTokenRefreshView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [
    # 🔑 Auth
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),

    # 👤 User Profile & Admin
    path("me/", ProfileView.as_view(), name="me"),
    path("users/", UserListView.as_view(), name="user_list"),

    # 🔒 Password Reset
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
