from django.urls import path

from .auth_views import (
    CookieLoginView,
    CookieRefreshView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterAccountView,
    VerifyEmailView,
)
from .health import HealthView, MetricsView
from .views import (
    CVPdfView,
    EducationDetailView,
    EducationListCreateView,
    ExperienceDetailView,
    ExperienceListCreateView,
    MeView,
    ProfileView,
    SkillDetailView,
    SkillListCreateView,
)

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("metrics/", MetricsView.as_view(), name="metrics"),
    path("register/", RegisterAccountView.as_view(), name="register"),
    path("login/", CookieLoginView.as_view(), name="login"),
    path("refresh/", CookieRefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("me/", MeView.as_view(), name="me"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/cv.pdf", CVPdfView.as_view(), name="cv-pdf"),
    path("experiences/", ExperienceListCreateView.as_view(), name="experiences"),
    path("experiences/<int:pk>/", ExperienceDetailView.as_view(), name="experience-detail"),
    path("educations/", EducationListCreateView.as_view(), name="educations"),
    path("educations/<int:pk>/", EducationDetailView.as_view(), name="education-detail"),
    path("skills/", SkillListCreateView.as_view(), name="skills"),
    path("skills/<int:pk>/", SkillDetailView.as_view(), name="skill-detail"),
]
