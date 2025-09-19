from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    ListAPIView,
    GenericAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserListSerializer,
    JWTTokenSerializer,
    get_tokens_for_user,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer,
)

User = get_user_model()


# ---------------------------
# Auth & Profile Views
# ---------------------------

class RegisterView(APIView):
    """Register a new user and return JWT tokens."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token_data = JWTTokenSerializer.from_user(user).data
        return Response(token_data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login user and return JWT tokens."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token_data = JWTTokenSerializer.from_user(user).data
        return Response(token_data, status=status.HTTP_200_OK)


class ProfileView(RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """Blacklist refresh token (logout)."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """Return new access token given a valid refresh token."""
    pass


# ---------------------------
# Password Reset Views
# ---------------------------

class PasswordResetRequestView(GenericAPIView):
    """Request a password reset link by email."""
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        # ✅ send frontend-friendly link
        reset_link = f"{settings.FRONTEND_URL}/auth/reset-password?uid={uidb64}&token={token}"

        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({"detail": "Password reset link sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(GenericAPIView):
    """Confirm password reset and set a new password."""
    serializer_class = SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)


# ---------------------------
# Admin User Management Views
# ---------------------------

class UserListView(ListAPIView):
    """Admin: list all users."""
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(RetrieveAPIView):
    """Admin: retrieve user details."""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


class UserUpdateView(RetrieveUpdateAPIView):
    """Admin: update user roles/permissions or profile."""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


class UserDeleteView(DestroyAPIView):
    """Admin: delete a user."""
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"
