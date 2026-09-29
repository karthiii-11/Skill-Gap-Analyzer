from django.contrib import admin
from .models import CareerTrack, Skill, RoleSkillRequirement

admin.site.register(CareerTrack)
admin.site.register(Skill)
admin.site.register(RoleSkillRequirement)