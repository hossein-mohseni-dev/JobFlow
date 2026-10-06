from django.contrib.auth.models import User
from django.db import models

from apps.jobs.models import Company, Job


class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        TECHNICAL_TEST = "technical_test", "Technical Test"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.APPLIED)
    note = models.TextField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "job")
        ordering = ["-updated_at"]
        indexes = [models.Index(fields=["user", "status"]), models.Index(fields=["deadline"])]

    def __str__(self):
        return f"{self.user.username} → {self.job.title} ({self.status})"


class SavedCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_companies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="saves")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "company")
        ordering = ["-created_at"]


class CompanyNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company_notes")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="notes")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=160)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_jobs")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saves")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job")
        ordering = ["-created_at"]


class Interview(models.Model):
    class Kind(models.TextChoices):
        PHONE = "phone", "Phone"
        VIDEO = "video", "Video"
        ONSITE = "onsite", "Onsite"
        TECHNICAL = "technical", "Technical"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interviews")
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="interviews")
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.VIDEO)
    starts_at = models.DateTimeField()
    location = models.CharField(max_length=160, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["starts_at"]


class CoverLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cover_letters")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="cover_letters")
    title = models.CharField(max_length=160)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
