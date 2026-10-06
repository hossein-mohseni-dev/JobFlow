from django.test import SimpleTestCase

from apps.jobs.matching import match_job


class Skill:
    def __init__(self, name):
        self.name = name


class Profile:
    def __init__(self):
        self.city = "Berlin"
        self.skills = self

    def all(self):
        return [Skill("postgres"), Skill("Django")]


class Job:
    title = "Backend Engineer"
    location = "Berlin"
    workplace = "hybrid"
    tags = "PostgreSQL,Django"
    requirements = "Django and PostgreSQL"
    description = "API work"


class MatchAlgorithmTests(SimpleTestCase):
    def test_synonym_and_breakdown(self):
        result = match_job(Profile(), Job())
        self.assertGreaterEqual(result["score"], 70)
        self.assertIn("postgresql", result["matched_skills"])
        self.assertIn("skills", result["breakdown"])
        self.assertIn("location", result["breakdown"])
