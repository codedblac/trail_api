from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
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

    # 👤 User Profile
    path("me/", ProfileView.as_view(), name="me"),

    # 👥 Admin User Management
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:id>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:id>/update/", UserUpdateView.as_view(), name="user_update"),
    path("users/<int:id>/delete/", UserDeleteView.as_view(), name="user_delete"),

    # 🔒 Password Reset
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
