import time

from django.core.cache import cache
from django.db import connection
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

STARTED = time.time()


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = []

    def get(self, request):
        checks = {"database": "ok", "cache": "ok"}
        status_code = 200
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception as exc:
            checks["database"] = str(exc)
            status_code = 503
        try:
            cache.set("jobflow-health", "1", 5)
            if cache.get("jobflow-health") != "1":
                raise RuntimeError("cache read failed")
        except Exception as exc:
            checks["cache"] = str(exc)
            status_code = 503
        payload = {
            "status": "ok" if status_code == 200 else "degraded",
            "service": "jobflow",
            "uptime_seconds": int(time.time() - STARTED),
            "checks": checks,
        }
        return Response(payload, status=status_code)


class MetricsView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = []

    def get(self, request):
        from apps.jobs.models import Job
        from apps.tracker.models import Application

        body = "\n".join(
            [
                "# HELP jobflow_up JobFlow process up",
                "# TYPE jobflow_up gauge",
                "jobflow_up 1",
                "# HELP jobflow_uptime_seconds Process uptime",
                "# TYPE jobflow_uptime_seconds gauge",
                f"jobflow_uptime_seconds {int(time.time() - STARTED)}",
                "# HELP jobflow_jobs Active jobs",
                "# TYPE jobflow_jobs gauge",
                f"jobflow_jobs {Job.objects.filter(is_active=True).count()}",
                "# HELP jobflow_applications Applications",
                "# TYPE jobflow_applications gauge",
                f"jobflow_applications {Application.objects.count()}",
            ]
        )
        return Response(body, content_type="text/plain")
