from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.accounts.models import Skill
from apps.jobs.models import Company, Job


SEED = [
    {
        "company": {
            "name": "Northline",
            "industry": "Fintech",
            "website": "https://example.com/northline",
            "location": "Berlin",
            "about": "Payments infrastructure for online businesses.",
            "logo_color": "#0f766e",
        },
        "jobs": [
            {
                "title": "Backend Engineer",
                "location": "Berlin",
                "employment_type": "full_time",
                "workplace": "hybrid",
                "salary_min": 70000,
                "salary_max": 95000,
                "currency": "EUR",
                "description": "Design APIs, tune queries, and ship with the product team.",
                "requirements": "Django, PostgreSQL, REST, tests",
                "tags": "Django,Python,PostgreSQL",
                "deadline_in": 12,
            },
            {
                "title": "Frontend Engineer",
                "location": "Remote",
                "employment_type": "full_time",
                "workplace": "remote",
                "salary_min": 68000,
                "salary_max": 90000,
                "currency": "EUR",
                "description": "Build dashboards and accessible product flows.",
                "requirements": "TypeScript, React, Tailwind",
                "tags": "Next.js,TypeScript,Tailwind",
                "deadline_in": 20,
            },
        ],
    },
    {
        "company": {
            "name": "Sepehr Cloud",
            "industry": "Cloud",
            "website": "https://example.com/sepehr",
            "location": "Amsterdam",
            "about": "Cloud tooling for product teams.",
            "logo_color": "#1d4ed8",
        },
        "jobs": [
            {
                "title": "DevOps Engineer",
                "location": "Amsterdam",
                "employment_type": "full_time",
                "workplace": "onsite",
                "salary_min": 75000,
                "salary_max": 100000,
                "currency": "EUR",
                "description": "Own CI/CD, monitoring, and container deploys.",
                "requirements": "Docker, GitHub Actions, Linux",
                "tags": "Docker,CI,Linux",
                "deadline_in": 7,
            }
        ],
    },
    {
        "company": {
            "name": "Rasad Data",
            "industry": "Analytics",
            "website": "https://example.com/rasad",
            "location": "Remote",
            "about": "Forecasting and retail analytics.",
            "logo_color": "#7c3aed",
        },
        "jobs": [
            {
                "title": "Data Intern",
                "location": "Remote",
                "employment_type": "internship",
                "workplace": "remote",
                "salary_min": 1800,
                "salary_max": 2400,
                "currency": "EUR",
                "description": "Clean data, build charts, and document experiments.",
                "requirements": "Python, pandas, curiosity",
                "tags": "Python,Data,Internship",
                "deadline_in": 5,
            }
        ],
    },
]


class Command(BaseCommand):
    help = "Seed companies, jobs, and the demo account"

    def handle(self, *args, **options):
        created_jobs = 0
        for block in SEED:
            company, _ = Company.objects.get_or_create(name=block["company"]["name"], defaults=block["company"])
            for job in block["jobs"]:
                payload = dict(job)
                days = payload.pop("deadline_in")
                _, created = Job.objects.get_or_create(
                    company=company,
                    title=payload["title"],
                    defaults={**payload, "deadline": date.today() + timedelta(days=days)},
                )
                created_jobs += int(created)
        user, created = User.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@jobflow.app", "first_name": "Demo", "last_name": "User"},
        )
        if created or not user.check_password("DemoPass123!"):
            user.set_password("DemoPass123!")
            user.email = "demo@jobflow.app"
            user.save()
        user.profile.email_verified = True
        user.profile.headline = "Full-stack engineer"
        user.profile.city = "Berlin"
        user.profile.summary = "I build Django APIs and Next.js products."
        user.profile.save()
        Skill.objects.get_or_create(profile=user.profile, name="Django", defaults={"level": 4})
        Skill.objects.get_or_create(profile=user.profile, name="TypeScript", defaults={"level": 4})
        self.stdout.write(self.style.SUCCESS(f"Seed complete. New jobs: {created_jobs}. Demo: demo / DemoPass123!"))
