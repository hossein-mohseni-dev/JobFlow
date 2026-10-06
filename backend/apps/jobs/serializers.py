from rest_framework import serializers

from .models import Company, Job


class CompanySerializer(serializers.ModelSerializer):
    open_roles = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ("id", "name", "industry", "website", "location", "about", "logo_color", "open_roles")

    def get_open_roles(self, obj):
        annotated = getattr(obj, "open_roles", None)
        if annotated is not None and not callable(annotated):
            return annotated
        return obj.jobs.filter(is_active=True).count()


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        source="company", queryset=Company.objects.all(), write_only=True, required=False
    )
    applied = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()
    match_score = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "company",
            "company_id",
            "location",
            "employment_type",
            "workplace",
            "salary_min",
            "salary_max",
            "currency",
            "description",
            "requirements",
            "tags",
            "deadline",
            "is_active",
            "created_at",
            "applied",
            "saved",
            "match_score",
        )

    def get_applied(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.applications.filter(user=request.user).exists()

    def get_saved(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.saves.filter(user=request.user).exists()

    def get_match_score(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None
        from .matching import match_job

        return match_job(request.user.profile, obj)["score"]
