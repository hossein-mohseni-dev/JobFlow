from datetime import date, timedelta

from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsEmailVerified
from apps.jobs.matching import match_job
from apps.jobs.models import Company, Job

from .models import Application, CompanyNote, CoverLetter, Interview, Notification, SavedCompany, SavedJob
from .serializers import (
    ApplicationSerializer,
    ApplicationUpdateSerializer,
    CompanyNoteSerializer,
    CoverLetterSerializer,
    InterviewSerializer,
    NotificationSerializer,
    SavedCompanySerializer,
    SavedJobSerializer,
)


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsEmailVerified()]
        return super().get_permissions()

    def get_queryset(self):
        qs = Application.objects.filter(user=self.request.user).select_related("job", "job__company")
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def create(self, request, *args, **kwargs):
        job = get_object_or_404(Job, pk=request.data.get("job_id"), is_active=True)
        if Application.objects.filter(user=request.user, job=job).exists():
            return Response({"detail": "You already applied to this role."}, status=400)
        application = Application.objects.create(
            user=request.user,
            job=job,
            note=request.data.get("note", ""),
            deadline=request.data.get("deadline") or job.deadline,
        )
        notify(request.user, "Application saved", f"You applied to {job.title} at {job.company.name}.")
        return Response(ApplicationSerializer(application, context={"request": request}).data, status=201)


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ApplicationUpdateSerializer
        return ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        old = instance.status
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if old != instance.status:
            notify(request.user, "Status updated", f"{instance.job.title} moved from {old} to {instance.status}.")
        return Response(ApplicationSerializer(instance, context={"request": request}).data)


class SaveCompanyView(APIView):
    def post(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        saved, created = SavedCompany.objects.get_or_create(user=request.user, company=company)
        if created:
            notify(request.user, "Company saved", f"{company.name} was added to saved companies.")
        return Response(SavedCompanySerializer(saved).data, status=201 if created else 200)

    def delete(self, request, pk):
        SavedCompany.objects.filter(user=request.user, company_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SavedCompanyListView(generics.ListAPIView):
    serializer_class = SavedCompanySerializer

    def get_queryset(self):
        return SavedCompany.objects.filter(user=self.request.user).select_related("company")


class CompanyNoteListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanyNoteSerializer

    def get_queryset(self):
        qs = CompanyNote.objects.filter(user=self.request.user)
        company_id = self.request.query_params.get("company")
        if company_id:
            qs = qs.filter(company_id=company_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyNoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyNoteSerializer

    def get_queryset(self):
        return CompanyNote.objects.filter(user=self.request.user)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationReadView(APIView):
    def post(self, request, pk=None):
        qs = Notification.objects.filter(user=request.user, is_read=False)
        if pk:
            qs = qs.filter(pk=pk)
        updated = qs.update(is_read=True)
        return Response({"updated": updated})


class DashboardView(APIView):
    def get(self, request):
        apps = Application.objects.filter(user=request.user)
        by_status = {row["status"]: row["total"] for row in apps.values("status").annotate(total=Count("id"))}
        upcoming = apps.filter(deadline__isnull=False, deadline__gte=date.today()).order_by("deadline")[:6]
        return Response(
            {
                "totals": {
                    "applications": apps.count(),
                    "saved_companies": SavedCompany.objects.filter(user=request.user).count(),
                    "unread_notifications": Notification.objects.filter(
                        user=request.user, is_read=False
                    ).count(),
                    "due_soon": apps.filter(
                        deadline__gte=date.today(), deadline__lte=date.today() + timedelta(days=7)
                    ).count(),
                },
                "by_status": [
                    {"status": key, "label": label, "total": by_status.get(key, 0)}
                    for key, label in Application.Status.choices
                ],
                "upcoming_deadlines": [
                    {
                        "id": item.id,
                        "title": item.job.title,
                        "company": item.job.company.name,
                        "status": item.status,
                        "deadline": item.deadline,
                    }
                    for item in upcoming
                ],
            }
        )


def notify(user, title, body, email=False):
    Notification.objects.create(user=user, title=title, body=body)
    if email and user.email:
        from django.conf import settings
        from django.core.mail import send_mail

        send_mail(title, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)


class SaveJobView(APIView):
    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
        return Response(SavedJobSerializer(saved, context={"request": request}).data, status=201 if created else 200)

    def delete(self, request, pk):
        SavedJob.objects.filter(user=request.user, job_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SavedJobListView(generics.ListAPIView):
    serializer_class = SavedJobSerializer

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user).select_related("job", "job__company")


class InterviewListCreateView(generics.ListCreateAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        return Interview.objects.filter(user=self.request.user).select_related("application__job__company")

    def perform_create(self, serializer):
        application = serializer.validated_data["application"]
        if application.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Not your application")
        interview = serializer.save(user=self.request.user)
        notify(
            self.request.user,
            "Interview scheduled",
            f"{interview.kind} interview for {application.job.title} at {interview.starts_at}.",
            email=True,
        )


class InterviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        return Interview.objects.filter(user=self.request.user)


class CalendarView(APIView):
    def get(self, request):
        interviews = Interview.objects.filter(user=request.user).select_related("application__job__company")
        deadlines = Application.objects.filter(user=request.user, deadline__isnull=False).select_related("job")
        events = [
            {
                "type": "interview",
                "id": item.id,
                "title": f"{item.application.job.title} ({item.kind})",
                "when": item.starts_at,
                "location": item.location,
            }
            for item in interviews
        ] + [
            {
                "type": "deadline",
                "id": item.id,
                "title": f"Deadline: {item.job.title}",
                "when": item.deadline,
                "location": "",
            }
            for item in deadlines
        ]
        events.sort(key=lambda event: str(event["when"]))
        return Response(events)


class CoverLetterListCreateView(generics.ListCreateAPIView):
    serializer_class = CoverLetterSerializer

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CoverLetterDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CoverLetterSerializer

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)


class CoverLetterDraftView(APIView):
    def post(self, request):
        job = get_object_or_404(Job, pk=request.data.get("job_id"))
        profile = request.user.profile
        analysis = match_job(profile, job)
        name = request.user.get_full_name() or request.user.username
        skills = ", ".join(analysis["matched_skills"]) or "relevant product skills"
        body = (
            f"Dear {job.company.name} hiring team,\n\n"
            f"I am {name}, {profile.headline or 'a software candidate'}. "
            f"I am applying for {job.title}. {profile.summary or 'I enjoy shipping reliable software.'}\n\n"
            f"My closest overlap is {skills}.\n\nThank you for your time.\n{name}"
        )
        letter = CoverLetter.objects.create(
            user=request.user, job=job, title=f"Cover letter — {job.title}", body=body
        )
        return Response(CoverLetterSerializer(letter).data, status=201)


class AnalyticsView(APIView):
    def get(self, request):
        apps = Application.objects.filter(user=request.user).select_related("job", "job__company")
        total = apps.count()
        by_status = {row["status"]: row["total"] for row in apps.values("status").annotate(total=Count("id"))}
        interviews = Interview.objects.filter(user=request.user).count()
        offers = by_status.get("offer", 0)
        rejected = by_status.get("rejected", 0)
        decided = offers + rejected
        weekly = {}
        for item in apps:
            key = item.applied_at.strftime("%Y-%W")
            weekly[key] = weekly.get(key, 0) + 1
        companies = {}
        for item in apps:
            companies[item.job.company.name] = companies.get(item.job.company.name, 0) + 1
        scores = [match_job(request.user.profile, item.job)["score"] for item in apps]
        return Response(
            {
                "applications": total,
                "interviews": interviews,
                "offers": offers,
                "offer_rate": round(offers / total, 2) if total else 0,
                "interview_rate": round(by_status.get("interview", 0) / total, 2) if total else 0,
                "win_rate": round(offers / decided, 2) if decided else 0,
                "saved_jobs": SavedJob.objects.filter(user=request.user).count(),
                "average_match": round(sum(scores) / len(scores), 1) if scores else 0,
                "funnel": [
                    {"stage": key, "total": by_status.get(key, 0)}
                    for key, _label in Application.Status.choices
                ],
                "weekly": [{"week": week, "applications": count} for week, count in sorted(weekly.items())],
                "by_company": [
                    {"company": name, "applications": count}
                    for name, count in sorted(companies.items(), key=lambda row: row[1], reverse=True)[:6]
                ],
            }
        )
