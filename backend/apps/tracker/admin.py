from django.contrib import admin

from .models import Application, CompanyNote, Notification, SavedCompany


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "status", "deadline")
    list_filter = ("status",)


admin.site.register(SavedCompany)
admin.site.register(CompanyNote)
admin.site.register(Notification)
