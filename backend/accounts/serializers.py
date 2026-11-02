from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import StudentProfile, User


class ProfileSerializer(serializers.ModelSerializer):
    target_career = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = [
            "full_name",
            "headline",
            "bio",
            "college",
            "graduation_year",
            "target_career",
        ]

    def get_target_career(self, profile):
        career = profile.target_career
        if career is None:
            return None
        return {"slug": career.slug, "title": career.title}


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["full_name", "headline", "bio", "college", "graduation_year"]

    def validate_graduation_year(self, value):
        if value is not None and not 2000 <= value <= 2045:
            raise serializers.ValidationError("Enter a year between 2000 and 2045.")
        return value


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    full_name = serializers.CharField(max_length=120)
    college = serializers.CharField(max_length=160, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("That username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("That email is already registered.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated):
        full_name = validated["full_name"].strip()
        first, _, last = full_name.partition(" ")
        user = User.objects.create_user(
            username=validated["username"],
            email=validated["email"],
            password=validated["password"],
            first_name=first,
            last_name=last,
        )
        profile = user.profile
        profile.full_name = full_name
        profile.college = validated.get("college", "")
        profile.save(update_fields=["full_name", "college"])
        return user
