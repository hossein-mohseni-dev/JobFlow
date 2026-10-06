from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .cookies import clear_auth_cookies, set_auth_cookies
from .emails import send_password_reset, send_verification, valid_reset
from .models import EmailVerification
from .serializers import RegisterSerializer


class CookieLoginView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            set_auth_cookies(response, response.data["access"], response.data["refresh"])
        return response


class CookieRefreshView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        refresh = request.COOKIES.get("jobflow_refresh") or request.data.get("refresh")
        serializer = TokenRefreshSerializer(data={"refresh": refresh})
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data["access"]
        new_refresh = serializer.validated_data.get("refresh", refresh)
        response = Response({"access": access, "refresh": new_refresh})
        set_auth_cookies(response, access, new_refresh)
        return response


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        response = Response({"detail": "Logged out"})
        clear_auth_cookies(response)
        return response


class RegisterAccountView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.email:
            send_verification(user)
        return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("token", "")
        record = EmailVerification.objects.filter(token=token, used_at__isnull=True).select_related("user").first()
        if not record:
            return Response({"detail": "Invalid verification token."}, status=400)
        record.used_at = timezone.now()
        record.save(update_fields=["used_at"])
        record.user.profile.email_verified = True
        record.user.profile.save(update_fields=["email_verified"])
        return Response({"detail": "Email verified."})


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        email = request.data.get("email", "")
        user = User.objects.filter(email__iexact=email).first()
        if user:
            send_password_reset(user)
        return Response({"detail": "If the account exists, a reset email was sent."})


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        reset = valid_reset(request.data.get("token", ""))
        password = request.data.get("password", "")
        if not reset or len(password) < 8:
            return Response({"detail": "Invalid token or password."}, status=400)
        reset.user.set_password(password)
        reset.user.save()
        reset.used_at = timezone.now()
        reset.save(update_fields=["used_at"])
        return Response({"detail": "Password updated."})
