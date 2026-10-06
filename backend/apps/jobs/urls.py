from django.urls import path

from .views import (
    CompanyDetailView,
    CompanyListView,
    JobAnalyzeView,
    JobDetailView,
    JobListView,
    RecommendationView,
)

urlpatterns = [
    path("jobs/", JobListView.as_view(), name="jobs"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    path("jobs/<int:pk>/analyze/", JobAnalyzeView.as_view(), name="job-analyze"),
    path("recommendations/", RecommendationView.as_view(), name="recommendations"),
    path("companies/", CompanyListView.as_view(), name="companies"),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
]
