from django.contrib import admin

from .models import Career, CareerSkill, RoadmapStage, RoadmapStep, Skill, SkillCategory, StepProgress, StudentSkill


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug")
    list_filter = ("category",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class CareerSkillInline(admin.TabularInline):
    model = CareerSkill
    extra = 0
    autocomplete_fields = ("skill",)


class RoadmapStageInline(admin.TabularInline):
    model = RoadmapStage
    extra = 0
    show_change_link = True


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("title", "outlook", "salary_range")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CareerSkillInline, RoadmapStageInline]


class RoadmapStepInline(admin.TabularInline):
    model = RoadmapStep
    extra = 0
    autocomplete_fields = ("skill",)


@admin.register(RoadmapStage)
class RoadmapStageAdmin(admin.ModelAdmin):
    list_display = ("title", "career", "sort_order", "weeks")
    list_filter = ("career",)
    inlines = [RoadmapStepInline]


@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    list_display = ("student", "skill", "level", "updated_at")
    list_filter = ("level", "skill__category")
    search_fields = ("student__username", "skill__name")


@admin.register(StepProgress)
class StepProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "step", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("student__username", "step__title")
