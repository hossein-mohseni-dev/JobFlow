from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=160, unique=True)
    industry = models.CharField(max_length=80, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=80, blank=True)
    about = models.TextField(blank=True)
    logo_color = models.CharField(max_length=7, default="#0f766e")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Job(models.Model):
    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT = "contract", "Contract"
        INTERNSHIP = "internship", "Internship"

    class Workplace(models.TextChoices):
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"
        ONSITE = "onsite", "Onsite"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=160)
    location = models.CharField(max_length=80)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
    workplace = models.CharField(max_length=20, choices=Workplace.choices)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=8, default="IRR")
    description = models.TextField()
    requirements = models.TextField(blank=True)
    tags = models.CharField(max_length=240, blank=True)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "deadline"]),
            models.Index(fields=["employment_type", "workplace"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.title} @ {self.company.name}"
