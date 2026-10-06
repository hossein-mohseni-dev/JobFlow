import secrets

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from .models import EmailVerification, PasswordReset


def frontend_url(path):
    return f"{settings.FRONTEND_URL.rstrip('/')}/{path.lstrip('/')}"


def send_verification(user):
    token = secrets.token_urlsafe(32)
    EmailVerification.objects.create(user=user, token=token)
    link = frontend_url(f"verify-email?token={token}")
    send_mail(
        "Verify your JobFlow email",
        f"Open this link to verify your account: {link}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
    return token


def send_password_reset(user):
    token = secrets.token_urlsafe(32)
    PasswordReset.objects.create(user=user, token=token)
    link = frontend_url(f"reset-password?token={token}")
    send_mail(
        "Reset your JobFlow password",
        f"This link expires in 2 hours: {link}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
    return token


def valid_reset(token):
    reset = PasswordReset.objects.filter(token=token, used_at__isnull=True).select_related("user").first()
    if not reset:
        return None
    if reset.created_at < timezone.now() - timedelta(hours=2):
        return None
    return reset
