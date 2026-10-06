from datetime import date, timedelta

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from apps.jobs.models import Company, Job
from apps.tracker.models import Application, Notification


class JobFlowApiTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="تست‌کو", industry="نرم‌افزار", location="تهران")
        self.job = Job.objects.create(
            company=self.company,
            title="بک‌اند",
            location="تهران",
            employment_type="full_time",
            workplace="remote",
            description="ساخت API",
            requirements="Django",
            tags="Django",
            deadline=date.today() + timedelta(days=3),
        )

    def test_register_login_apply_and_dashboard(self):
        register = self.client.post(
            "/api/auth/register/",
            {
                "username": "sara",
                "email": "sara@example.com",
                "password": "strongpass1",
                "first_name": "سارا",
                "last_name": "نمونه",
            },
            format="json",
        )
        self.assertEqual(register.status_code, 201)
        user = User.objects.get(username="sara")
        user.profile.email_verified = True
        user.profile.save()
        Skill = user.profile.skills.model
        Skill.objects.create(profile=user.profile, name="Django", level=4)

        login = self.client.post(
            "/api/auth/login/",
            {"username": "sara", "password": "strongpass1"},
            format="json",
        )
        self.assertEqual(login.status_code, 200)
        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        jobs = self.client.get("/api/jobs/?search=بک")
        self.assertEqual(jobs.status_code, 200)
        self.assertGreaterEqual(jobs.data["count"], 1)

        apply = self.client.post("/api/applications/", {"job_id": self.job.id, "note": "علاقه‌مندم"}, format="json")
        self.assertEqual(apply.status_code, 201)
        app_id = apply.data["id"]

        patch = self.client.patch(
            f"/api/applications/{app_id}/",
            {"status": "interview"},
            format="json",
        )
        self.assertEqual(patch.status_code, 200)
        self.assertEqual(patch.data["status"], "interview")

        save = self.client.post(f"/api/companies/{self.company.id}/save/")
        self.assertIn(save.status_code, (200, 201))

        note = self.client.post(
            "/api/notes/",
            {"company": self.company.id, "body": "فرهنگ تیمی خوب به نظر می‌رسد."},
            format="json",
        )
        self.assertEqual(note.status_code, 201)

        stats = self.client.get("/api/dashboard/")
        self.assertEqual(stats.status_code, 200)
        self.assertEqual(stats.data["totals"]["applications"], 1)
        self.assertEqual(stats.data["totals"]["saved_companies"], 1)

        pdf = self.client.get("/api/v1/auth/profile/cv.pdf?template=modern")
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf["Content-Type"], "application/pdf")
        analyze = self.client.get(f"/api/v1/jobs/{self.job.id}/analyze/")
        self.assertEqual(analyze.status_code, 200)
        self.assertIn("score", analyze.data)
        save_job = self.client.post(f"/api/v1/jobs/{self.job.id}/save/")
        self.assertIn(save_job.status_code, (200, 201))
        self.assertTrue(Notification.objects.filter(user__username="sara").exists())
        self.assertEqual(Application.objects.get(pk=app_id).status, "interview")
