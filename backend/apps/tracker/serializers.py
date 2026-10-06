from rest_framework import serializers

from apps.jobs.serializers import CompanySerializer, JobSerializer

from .models import Application, CompanyNote, CoverLetter, Interview, Notification, SavedCompany, SavedJob


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Application
        fields = (
            "id",
            "job",
            "job_id",
            "status",
            "note",
            "deadline",
            "applied_at",
            "updated_at",
        )
        read_only_fields = ("applied_at", "updated_at")


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "status", "note", "deadline", "updated_at")
        read_only_fields = ("updated_at",)


class SavedCompanySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = SavedCompany
        fields = ("id", "company", "created_at")


class CompanyNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyNote
        fields = ("id", "company", "body", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "body", "is_read", "created_at")


class SavedJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = SavedJob
        fields = ("id", "job", "created_at")


class InterviewSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="application.job.title", read_only=True)
    company_name = serializers.CharField(source="application.job.company.name", read_only=True)

    class Meta:
        model = Interview
        fields = ("id", "application", "kind", "starts_at", "location", "notes", "job_title", "company_name", "created_at")
        read_only_fields = ("created_at",)


class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ("id", "job", "title", "body", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")
