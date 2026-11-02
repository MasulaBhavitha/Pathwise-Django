from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=120)
    headline = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    college = models.CharField(max_length=160, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    target_career = models.ForeignKey(
        "catalog.Career",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="students",
    )

    def __str__(self):
        return self.full_name or self.user.username


def ensure_profile(user):
    profile, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={"full_name": user.get_full_name() or user.username},
    )
    return profile
