from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from accounts.models import StudentProfile
from catalog.models import (
    Career,
    CareerSkill,
    RoadmapStage,
    RoadmapStep,
    Skill,
    SkillCategory,
    StepProgress,
    StudentSkill,
)
from catalog.seed_data import CAREERS, CATEGORIES, SKILLS

User = get_user_model()

DEMO_LEVELS = {
    "html-css": 3,
    "javascript": 2,
    "react": 1,
    "git": 2,
    "communication": 3,
    "problem-solving": 3,
    "python": 2,
    "sql": 1,
    "accessibility": 2,
}


class Command(BaseCommand):
    help = "Load skill categories, careers, roadmaps, and the demo student."

    def handle(self, *args, **options):
        skills = self._load_skills()
        self._load_careers(skills)
        self._load_demo(skills)
        self._load_admin()
        self.stdout.write(self.style.SUCCESS("Catalog ready. Demo login: demo / pathwise123"))

    def _load_skills(self):
        categories = {}
        for category in CATEGORIES:
            record, _ = SkillCategory.objects.update_or_create(
                slug=category["slug"],
                defaults={
                    "name": category["name"],
                    "description": category["description"],
                    "sort_order": category["sort_order"],
                },
            )
            categories[category["slug"]] = record

        skills = {}
        for category_slug, slug, name, description in SKILLS:
            record, _ = Skill.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": description,
                    "category": categories[category_slug],
                },
            )
            skills[slug] = record
        return skills

    def _load_careers(self, skills):
        for career_data in CAREERS:
            career, _ = Career.objects.update_or_create(
                slug=career_data["slug"],
                defaults={
                    "title": career_data["title"],
                    "summary": career_data["summary"],
                    "description": career_data["description"],
                    "outlook": career_data["outlook"],
                    "salary_range": career_data["salary_range"],
                    "accent": career_data["accent"],
                },
            )
            seen_skills = []
            for slug, level, importance in career_data["requirements"]:
                skill = skills.get(slug)
                if skill is None:
                    raise CommandError(f"Unknown skill slug '{slug}' on {career.slug}")
                CareerSkill.objects.update_or_create(
                    career=career,
                    skill=skill,
                    defaults={"required_level": level, "importance": importance},
                )
                seen_skills.append(skill.id)
            career.requirements.exclude(skill_id__in=seen_skills).delete()

            for index, stage_data in enumerate(career_data["stages"]):
                stage, _ = RoadmapStage.objects.update_or_create(
                    career=career,
                    sort_order=index,
                    defaults={
                        "title": stage_data["title"],
                        "summary": stage_data["summary"],
                        "weeks": stage_data["weeks"],
                    },
                )
                for step_index, step_data in enumerate(stage_data["steps"]):
                    skill = None
                    if step_data["skill"]:
                        skill = skills.get(step_data["skill"])
                        if skill is None:
                            raise CommandError(
                                f"Unknown skill slug '{step_data['skill']}' on step '{step_data['title']}'"
                            )
                    RoadmapStep.objects.update_or_create(
                        stage=stage,
                        sort_order=step_index,
                        defaults={
                            "title": step_data["title"],
                            "detail": step_data["detail"],
                            "skill": skill,
                            "resource_label": step_data["resource_label"],
                            "resource_url": step_data["resource_url"],
                        },
                    )
                stage.steps.filter(sort_order__gte=len(stage_data["steps"])).delete()
            career.stages.filter(sort_order__gte=len(career_data["stages"])).delete()

    def _load_demo(self, skills):
        user, _ = User.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@pathwise.local", "first_name": "Maya", "last_name": "Chen"},
        )
        user.email = "demo@pathwise.local"
        user.first_name = "Maya"
        user.last_name = "Chen"
        user.set_password("pathwise123")
        user.save()

        profile, _ = StudentProfile.objects.get_or_create(user=user, defaults={"full_name": "Maya Chen"})
        profile.full_name = "Maya Chen"
        profile.headline = "Second-year CS student aiming at frontend engineering"
        profile.bio = (
            "I like building interfaces and I want a roadmap that shows the gap between class projects and a job."
        )
        profile.college = "Northbridge University"
        profile.graduation_year = 2028
        profile.target_career = Career.objects.get(slug="frontend-engineer")
        profile.save()

        for slug, level in DEMO_LEVELS.items():
            StudentSkill.objects.update_or_create(
                student=user,
                skill=skills[slug],
                defaults={"level": level},
            )

        steps = list(
            RoadmapStep.objects.filter(stage__career__slug="frontend-engineer").order_by(
                "stage__sort_order", "sort_order"
            )
        )
        statuses = [
            StepProgress.Status.COMPLETED,
            StepProgress.Status.COMPLETED,
            StepProgress.Status.IN_PROGRESS,
        ]
        for step_record, status in zip(steps, statuses):
            StepProgress.objects.update_or_create(
                student=user,
                step=step_record,
                defaults={"status": status},
            )

    def _load_admin(self):
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@pathwise.local", "is_staff": True, "is_superuser": True},
        )
        admin.email = "admin@pathwise.local"
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("pathwise-admin")
        admin.save()
