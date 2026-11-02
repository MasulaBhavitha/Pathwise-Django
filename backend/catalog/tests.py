from django.test import TestCase
from rest_framework.test import APIClient

from catalog.models import Skill, SkillCategory
from catalog.services import analyze_requirements


class AnalyzeRequirementsTests(TestCase):
    def test_core_skills_weigh_more_than_recommended(self):
        requirements = [
            {
                "skill_id": 1,
                "skill_name": "JavaScript",
                "skill_slug": "javascript",
                "category": "Web",
                "required_level": 4,
                "importance": "core",
            },
            {
                "skill_id": 2,
                "skill_name": "Git",
                "skill_slug": "git",
                "category": "Programming",
                "required_level": 2,
                "importance": "recommended",
            },
        ]
        score, rows, gaps = analyze_requirements(requirements, {1: 2, 2: 2})
        self.assertEqual(score, 60)
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["gap"], 2)
        self.assertEqual(rows[1]["current_level"], 2)

    def test_empty_requirements_score_zero(self):
        score, rows, gaps = analyze_requirements([], {})
        self.assertEqual(score, 0)
        self.assertEqual(rows, [])
        self.assertEqual(gaps, [])


class SkillRatingApiTests(TestCase):
    def setUp(self):
        category = SkillCategory.objects.create(name="Programming", slug="programming")
        self.skill = Skill.objects.create(
            category=category, name="Python", slug="python", description="General programming."
        )
        self.client = APIClient()

    def test_register_and_rate_skill(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "ada",
                "email": "ada@example.com",
                "password": "pathwise123",
                "full_name": "Ada Lovelace",
                "college": "Analytical Engines",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        rated = self.client.put(
            "/api/me/skills/",
            {"skill_id": self.skill.id, "level": 4},
            format="json",
        )
        self.assertEqual(rated.status_code, 200)

        catalog = self.client.get("/api/skills/")
        self.assertEqual(catalog.status_code, 200)
        self.assertEqual(catalog.data[0]["skills"][0]["level"], 4)

        dashboard = self.client.get("/api/dashboard/")
        self.assertEqual(dashboard.data["skills_rated"], 1)
        self.assertIsNone(dashboard.data["target"])
