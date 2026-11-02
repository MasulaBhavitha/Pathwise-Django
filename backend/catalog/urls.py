from django.urls import path

from .views import (
    CareerDetailView,
    CareerListView,
    DashboardView,
    MetaView,
    SkillCatalogView,
    StepProgressView,
    StudentSkillView,
    TargetCareerView,
)

urlpatterns = [
    path("meta/", MetaView.as_view(), name="meta"),
    path("skills/", SkillCatalogView.as_view(), name="skills"),
    path("careers/", CareerListView.as_view(), name="careers"),
    path("careers/<slug:slug>/", CareerDetailView.as_view(), name="career-detail"),
    path("me/skills/", StudentSkillView.as_view(), name="student-skills"),
    path("me/target/", TargetCareerView.as_view(), name="target-career"),
    path("me/steps/<int:step_id>/", StepProgressView.as_view(), name="step-progress"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
