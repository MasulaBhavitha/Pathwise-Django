from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import ensure_profile
from .models import Career, CareerSkill, RoadmapStep, Skill, SkillCategory, StepProgress, StudentSkill
from .serializers import (
    StepProgressWriteSerializer,
    StudentSkillWriteSerializer,
    TargetCareerSerializer,
)
from .services import analyze_requirements, requirement_payload

LEVELS = [
    {"value": 0, "label": "Unrated"},
    {"value": 1, "label": "Aware"},
    {"value": 2, "label": "Beginner"},
    {"value": 3, "label": "Intermediate"},
    {"value": 4, "label": "Advanced"},
    {"value": 5, "label": "Expert"},
]


def student_levels(user):
    if not user.is_authenticated:
        return {}
    return dict(StudentSkill.objects.filter(student=user).values_list("skill_id", "level"))


def target_id(user):
    if not user.is_authenticated:
        return None
    return ensure_profile(user).target_career_id


def ordered_requirements(career):
    requirements = list(career.requirements.all())
    requirements.sort(
        key=lambda item: (
            0 if item.importance == CareerSkill.Importance.CORE else 1,
            -item.required_level,
            item.skill.name,
        )
    )
    return requirements


def career_summary(career, score, is_target):
    return {
        "slug": career.slug,
        "title": career.title,
        "summary": career.summary,
        "outlook": career.outlook,
        "salary_range": career.salary_range,
        "accent": career.accent,
        "readiness": score,
        "is_target": is_target,
        "core_skill_count": sum(
            1 for req in career.requirements.all() if req.importance == CareerSkill.Importance.CORE
        ),
    }


def progress_map(user, step_ids):
    if not user.is_authenticated or not step_ids:
        return {}
    return dict(
        StepProgress.objects.filter(student=user, step_id__in=step_ids).values_list(
            "step_id", "status"
        )
    )


def stage_payload(career, user):
    stages = list(career.stages.prefetch_related("steps__skill"))
    step_ids = [step.id for stage in stages for step in stage.steps.all()]
    statuses = progress_map(user, step_ids)
    payload = []
    for stage in stages:
        steps = []
        for step in stage.steps.all():
            steps.append(
                {
                    "id": step.id,
                    "title": step.title,
                    "detail": step.detail,
                    "skill_name": step.skill.name if step.skill_id else None,
                    "skill_slug": step.skill.slug if step.skill_id else None,
                    "resource_label": step.resource_label,
                    "resource_url": step.resource_url,
                    "status": statuses.get(step.id, StepProgress.Status.NOT_STARTED),
                }
            )
        payload.append(
            {
                "id": stage.id,
                "title": stage.title,
                "summary": stage.summary,
                "weeks": stage.weeks,
                "steps": steps,
            }
        )
    return payload


def scores_for_user(user):
    careers = list(Career.objects.prefetch_related("requirements__skill__category"))
    levels = student_levels(user)
    chosen = target_id(user)
    results = []
    for career in careers:
        reqs = [requirement_payload(item) for item in ordered_requirements(career)]
        score, rows, gaps = analyze_requirements(reqs, levels)
        results.append(
            {
                "career": career,
                "score": score,
                "rows": rows,
                "gaps": gaps,
                "is_target": career.id == chosen,
            }
        )
    return results


class MetaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"levels": LEVELS})


class SkillCatalogView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        levels = student_levels(request.user)
        categories = SkillCategory.objects.prefetch_related("skills")
        payload = []
        for category in categories:
            payload.append(
                {
                    "id": category.id,
                    "name": category.name,
                    "slug": category.slug,
                    "description": category.description,
                    "skills": [
                        {
                            "id": skill.id,
                            "name": skill.name,
                            "slug": skill.slug,
                            "description": skill.description,
                            "level": levels.get(skill.id, 0),
                        }
                        for skill in category.skills.all()
                    ],
                }
            )
        return Response(payload)


class CareerListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        payload = []
        for item in scores_for_user(request.user):
            payload.append(career_summary(item["career"], item["score"], item["is_target"]))
        payload.sort(key=lambda item: (-item["readiness"], item["title"]))
        return Response(payload)


class CareerDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        career = get_object_or_404(
            Career.objects.prefetch_related("requirements__skill__category", "stages__steps__skill"),
            slug=slug,
        )
        levels = student_levels(request.user)
        reqs = [requirement_payload(item) for item in ordered_requirements(career)]
        score, rows, gaps = analyze_requirements(reqs, levels)
        return Response(
            {
                **career_summary(career, score, career.id == target_id(request.user)),
                "description": career.description,
                "requirements": rows,
                "gaps": gaps[:6],
                "stages": stage_payload(career, request.user),
            }
        )


class StudentSkillView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = StudentSkillWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record, _ = StudentSkill.objects.update_or_create(
            student=request.user,
            skill_id=serializer.validated_data["skill_id"],
            defaults={"level": serializer.validated_data["level"]},
        )
        return Response({"skill_id": record.skill_id, "level": record.level})


class TargetCareerView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = TargetCareerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        slug = serializer.validated_data["career_slug"]
        profile = ensure_profile(request.user)
        if slug is None:
            profile.target_career = None
        else:
            profile.target_career = get_object_or_404(Career, slug=slug)
        profile.save(update_fields=["target_career"])
        career = profile.target_career
        return Response(
            {
                "target_career": None
                if career is None
                else {"slug": career.slug, "title": career.title}
            }
        )


class StepProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, step_id):
        step = get_object_or_404(RoadmapStep, pk=step_id)
        serializer = StepProgressWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data["status"]
        if status == StepProgress.Status.NOT_STARTED:
            StepProgress.objects.filter(student=request.user, step=step).delete()
        else:
            StepProgress.objects.update_or_create(
                student=request.user,
                step=step,
                defaults={"status": status},
            )
        return Response({"step_id": step.id, "status": status})


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        analyzed = scores_for_user(user)
        target = next((item for item in analyzed if item["is_target"]), None)
        suggestions = sorted(analyzed, key=lambda item: (-item["score"], item["career"].title))[:3]

        skills_total = Skill.objects.count()
        skills_rated = StudentSkill.objects.filter(student=user, level__gt=0).count()

        next_steps = []
        roadmap = {"completed": 0, "total": 0, "percent": 0}
        top_gaps = []
        target_payload = None

        if target is not None:
            career = target["career"]
            stages = stage_payload(career, user)
            flat_steps = [step for stage in stages for step in stage["steps"]]
            completed = sum(1 for step in flat_steps if step["status"] == StepProgress.Status.COMPLETED)
            total = len(flat_steps)
            roadmap = {
                "completed": completed,
                "total": total,
                "percent": round(100 * completed / total) if total else 0,
            }
            for stage in stages:
                for step in stage["steps"]:
                    if step["status"] != StepProgress.Status.COMPLETED:
                        next_steps.append({**step, "stage": stage["title"]})
                    if len(next_steps) == 3:
                        break
                if len(next_steps) == 3:
                    break
            top_gaps = [
                {
                    "skill_name": gap["skill_name"],
                    "skill_slug": gap["skill_slug"],
                    "current_level": gap["current_level"],
                    "required_level": gap["required_level"],
                    "gap": gap["gap"],
                    "importance": gap["importance"],
                }
                for gap in target["gaps"][:5]
            ]
            target_payload = {
                "slug": career.slug,
                "title": career.title,
                "summary": career.summary,
                "accent": career.accent,
                "outlook": career.outlook,
                "readiness": target["score"],
            }

        return Response(
            {
                "skills_rated": skills_rated,
                "skills_total": skills_total,
                "target": target_payload,
                "top_gaps": top_gaps,
                "next_steps": next_steps,
                "roadmap": roadmap,
                "suggestions": [
                    career_summary(item["career"], item["score"], item["is_target"])
                    for item in suggestions
                ],
            }
        )
