import django_filters
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .matching import match_job

from .models import Company, Job
from .serializers import CompanySerializer, JobSerializer


class JobFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    employment_type = django_filters.CharFilter(field_name="employment_type")
    workplace = django_filters.CharFilter(field_name="workplace")
    location = django_filters.CharFilter(field_name="location", lookup_expr="icontains")
    company = django_filters.NumberFilter(field_name="company_id")
    tag = django_filters.CharFilter(field_name="tags", lookup_expr="icontains")

    class Meta:
        model = Job
        fields = ["employment_type", "workplace", "location", "company", "tag"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(company__name__icontains=value)
            | Q(tags__icontains=value)
        )


class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = JobFilter
    search_fields = ["title", "company__name", "tags"]
    ordering_fields = ["created_at", "deadline", "title"]

    def get_queryset(self):
        return Job.objects.filter(is_active=True).select_related("company")


class JobDetailView(generics.RetrieveAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.select_related("company")


class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.annotate(open_roles=Count("jobs", filter=Q(jobs__is_active=True)))


class CompanyDetailView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.annotate(open_roles=Count("jobs", filter=Q(jobs__is_active=True)))


class JobAnalyzeView(APIView):
    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        return Response(match_job(request.user.profile, job) | {"job_id": job.id, "title": job.title})


class RecommendationView(APIView):
    def get(self, request):
        profile = request.user.profile
        ranked = []
        for job in Job.objects.filter(is_active=True).select_related("company"):
            analysis = match_job(profile, job)
            ranked.append({"job": JobSerializer(job, context={"request": request}).data, "analysis": analysis})
        ranked.sort(key=lambda item: item["analysis"]["score"], reverse=True)
        return Response(ranked[:8])
