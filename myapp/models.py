from django.db import models


class CareerTrack(models.Model):
    LEVEL_CHOICES = [
        ("FRESHER", "Fresher"),
        ("EXPERIENCED", "Experienced"),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="FRESHER")

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RoleSkillRequirement(models.Model):
    career_track = models.ForeignKey(CareerTrack, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.career_track.name} needs {self.skill.name}"