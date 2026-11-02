from django.conf import settings
from django.db import models


class SkillCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "skill categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(
        SkillCategory, related_name="skills", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = [("category", "name")]

    def __str__(self):
        return self.name


class Career(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=240)
    description = models.TextField()
    outlook = models.CharField(max_length=40)
    salary_range = models.CharField(max_length=40)
    accent = models.CharField(max_length=20, default="#c45c26")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class CareerSkill(models.Model):
    class Importance(models.TextChoices):
        CORE = "core", "Core"
        RECOMMENDED = "recommended", "Recommended"

    career = models.ForeignKey(Career, related_name="requirements", on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name="career_requirements", on_delete=models.CASCADE)
    required_level = models.PositiveSmallIntegerField()
    importance = models.CharField(
        max_length=20, choices=Importance.choices, default=Importance.CORE
    )

    class Meta:
        unique_together = [("career", "skill")]

    def __str__(self):
        return f"{self.career.title}: {self.skill.name}"


class RoadmapStage(models.Model):
    career = models.ForeignKey(Career, related_name="stages", on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    summary = models.CharField(max_length=280, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    weeks = models.PositiveSmallIntegerField(default=4)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.career.title} — {self.title}"


class RoadmapStep(models.Model):
    stage = models.ForeignKey(RoadmapStage, related_name="steps", on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    detail = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    skill = models.ForeignKey(
        Skill,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="steps",
    )
    resource_label = models.CharField(max_length=120, blank=True)
    resource_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title


class StudentSkill(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="skill_levels", on_delete=models.CASCADE
    )
    skill = models.ForeignKey(Skill, related_name="student_levels", on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("student", "skill")]

    def __str__(self):
        return f"{self.student} · {self.skill} · {self.level}"


class StepProgress(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not started"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="step_progress", on_delete=models.CASCADE
    )
    step = models.ForeignKey(RoadmapStep, related_name="progress", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NOT_STARTED
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("student", "step")]

    def __str__(self):
        return f"{self.student} · {self.step} · {self.status}"
