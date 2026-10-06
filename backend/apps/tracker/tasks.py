from datetime import date, timedelta

from celery import shared_task

from .models import Application, Notification


@shared_task
def send_deadline_reminders():
    horizon = date.today() + timedelta(days=2)
    due = Application.objects.filter(
        deadline__isnull=False,
        deadline__lte=horizon,
        deadline__gte=date.today(),
        reminder_sent=False,
    ).select_related("job", "job__company", "user")
    count = 0
    for app in due:
        Notification.objects.create(
            user=app.user,
            title="Deadline is close",
            body=f"The deadline for {app.job.title} at {app.job.company.name} is {app.deadline}.",
        )
        if app.user.email:
            from django.conf import settings
            from django.core.mail import send_mail

            send_mail(
                "JobFlow deadline reminder",
                f"{app.job.title} closes on {app.deadline}.",
                settings.DEFAULT_FROM_EMAIL,
                [app.user.email],
                fail_silently=True,
            )
        app.reminder_sent = True
        app.save(update_fields=["reminder_sent"])
        count += 1
    return count
