from rest_framework import serializers

from .models import StepProgress, StudentSkill


class StudentSkillWriteSerializer(serializers.Serializer):
    skill_id = serializers.IntegerField()
    level = serializers.IntegerField(min_value=0, max_value=5)

    def validate_skill_id(self, value):
        from .models import Skill

        if not Skill.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Unknown skill.")
        return value


class StepProgressWriteSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=StepProgress.Status.choices)


class TargetCareerSerializer(serializers.Serializer):
    career_slug = serializers.SlugField(allow_null=True, required=True)
