from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Education, Experience, Skill
from .serializers import (
    EducationSerializer,
    ExperienceSerializer,
    MeSerializer,
    ProfileSerializer,
    RegisterSerializer,
    SkillSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class ExperienceListCreateView(generics.ListCreateAPIView):
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        return self.request.user.profile.experiences.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        return self.request.user.profile.experiences.all()


class EducationListCreateView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer

    def get_queryset(self):
        return self.request.user.profile.educations.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer

    def get_queryset(self):
        return self.request.user.profile.educations.all()


class SkillListCreateView(generics.ListCreateAPIView):
    serializer_class = SkillSerializer

    def get_queryset(self):
        return self.request.user.profile.skills.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSerializer

    def get_queryset(self):
        return self.request.user.profile.skills.all()


class CVPdfView(APIView):
    def get(self, request):
        template = request.query_params.get("template", "classic")
        if template not in {"classic", "modern", "compact"}:
            template = "classic"
        profile = request.user.profile
        user = request.user
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="jobflow-cv-{template}.pdf"'
        pdf = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 48
        if template == "modern":
            pdf.setFillColorRGB(0.06, 0.46, 0.43)
            pdf.rect(0, height - 90, width, 90, fill=1, stroke=0)
            pdf.setFillColorRGB(1, 1, 1)
            y = height - 40
        elif template == "compact":
            y = height - 36
        pdf.setFont("Helvetica-Bold", 16 if template == "compact" else 18)
        name = f"{user.first_name} {user.last_name}".strip() or user.username
        pdf.drawString(48, y, name)
        y -= 18
        pdf.setFont("Helvetica", 10)
        pdf.drawString(48, y, profile.headline or "JobFlow CV")
        y -= 14
        meta = " | ".join(filter(None, [user.email, profile.phone, profile.city]))
        pdf.setFont("Helvetica", 8)
        pdf.drawString(48, y, meta[:120])
        if template == "modern":
            pdf.setFillColorRGB(0.06, 0.13, 0.12)
            y = height - 110
        else:
            y -= 18
            pdf.setStrokeColorRGB(0.12, 0.45, 0.42)
            pdf.line(48, y, width - 48, y)
            y -= 20

        def section(title):
            nonlocal y
            if y < 80:
                pdf.showPage()
                y = height - 48
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(48, y, title)
            y -= 14

        def paragraph(text, size=9):
            nonlocal y
            pdf.setFont("Helvetica", size)
            for raw in (text or "—").splitlines():
                line = raw
                while True:
                    if y < 48:
                        pdf.showPage()
                        y = height - 48
                    pdf.drawString(56, y, line[:110])
                    y -= 12
                    line = line[110:]
                    if not line:
                        break
            y -= 2

        section("SUMMARY")
        paragraph(profile.summary)
        section("EXPERIENCE")
        for item in profile.experiences.all():
            end = "Present" if item.current or not item.end_date else str(item.end_date)
            paragraph(f"{item.title} — {item.company} ({item.start_date} to {end})")
            if item.description:
                paragraph(item.description, 8)
        section("EDUCATION")
        for item in profile.educations.all():
            paragraph(f"{item.degree} in {item.field} — {item.school}")
        section("SKILLS")
        paragraph(", ".join(s.name for s in profile.skills.all()) or "—")
        pdf.setFont("Helvetica-Oblique", 8)
        pdf.drawString(48, 28, f"JobFlow {template} template")
        pdf.save()
        return response


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok", "service": "jobflow"}, status=status.HTTP_200_OK)
