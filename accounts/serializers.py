from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# 🔹 Utility to generate tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration (signup)."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "phone", "address", "city", "postal_code",
            "password", "password2"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating user profile (self)."""
    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "phone", "address",
            "city", "postal_code", "role", "date_joined"
        ]
        read_only_fields = ["id", "email", "role", "date_joined"]


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for admin/staff to list users."""
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "is_active", "date_joined"]


class AdminUserDetailSerializer(serializers.ModelSerializer):
    """Detailed view of a user (for admin)."""
    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "phone", "address",
            "city", "postal_code", "role", "is_active",
            "is_staff", "is_superuser", "date_joined"
        ]
        read_only_fields = ["id", "date_joined", "email"]


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for admin to update roles/permissions."""
    class Meta:
        model = User
        fields = ["role", "is_active", "is_staff", "is_superuser"]


class JWTTokenSerializer(serializers.Serializer):
    """Return user info + JWT tokens (used on login/register)."""
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    @classmethod
    def from_user(cls, user):
        tokens = get_tokens_for_user(user)
        return cls({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "access": tokens["access"],
            "refresh": tokens["refresh"],
        })


# 🔹 Password Reset Serializers
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No account with this email.")
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=6)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = smart_str(urlsafe_base64_decode(attrs["uidb64"]))
            user = User.objects.get(id=uid)
        except (User.DoesNotExist, DjangoUnicodeDecodeError):
            raise serializers.ValidationError("Invalid reset link.")

        if not PasswordResetTokenGenerator().check_token(user, attrs["token"]):
            raise serializers.ValidationError("Reset link is invalid or expired.")

        user.set_password(attrs["password"])
        user.save()
        return attrs
