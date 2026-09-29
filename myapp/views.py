from django.shortcuts import render, redirect
from .models import CareerTrack, Skill


SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "C", "C++"
    ],
    "Web Development": [
        "HTML", "CSS", "Django", "React", "Node.js", "REST API"
    ],
    "Data & AI": [
        "Pandas", "NumPy", "Machine Learning",
        "Excel", "Power BI", "Tableau"
    ],
    "Databases & Tools": [
        "SQL", "PostgreSQL", "MongoDB", "Git"
    ],
    "Cloud & DevOps": [
        "Docker", "AWS", "Linux", "CI/CD", "Cloud Architecture"
    ],
    "Professional Skills": [
        "Communication", "Problem Solving",
        "Data Structures & Algorithms"
    ],
    "Leadership & Design": [
        "System Design", "Team Leadership", "Mentoring"
    ],
}


def get_skill_categories(skills):
    categories = []
    added_skill_ids = set()

    for category_name, skill_names in SKILL_CATEGORIES.items():
        category_skills = []

        for skill in skills:
            if skill.name in skill_names:
                category_skills.append(skill)
                added_skill_ids.add(skill.id)

        if category_skills:
            categories.append({
                "name": category_name,
                "skills": category_skills,
            })

    remaining_skills = []

    for skill in skills:
        if skill.id not in added_skill_ids:
            remaining_skills.append(skill)

    if remaining_skills:
        categories.append({
            "name": "Other Skills",
            "skills": remaining_skills,
        })

    return categories


def landing(request):
    if request.method == "POST":
        name = request.POST.get("name")
        status = request.POST.get("status")

        request.session["user_name"] = name
        request.session["user_status"] = status

        return redirect("home")

    return render(request, "myapp/landing.html", {})


def home(request):
    career_tracks = CareerTrack.objects.all().order_by("name")
    skills = list(Skill.objects.all().order_by("name"))

    context = {
        "career_tracks": career_tracks,
        "skill_categories": get_skill_categories(skills),
        "user_name": request.session.get("user_name"),
        "user_status": request.session.get("user_status"),
    }

    if request.method == "POST":
        selected_role_id = request.POST.get("career_track")
        selected_skill_ids = request.POST.getlist("skills")

        selected_role = CareerTrack.objects.filter(
            id=selected_role_id
        ).first()

        if selected_role:
            required_skills = Skill.objects.filter(
                roleskillrequirement__career_track=selected_role
            ).distinct()

            selected_skill_ids = [
                int(skill_id) for skill_id in selected_skill_ids
            ]

            selected_skills = Skill.objects.filter(id__in=selected_skill_ids)

            matched_skills = required_skills.filter(
                id__in=selected_skill_ids
            )

            missing_skills = required_skills.exclude(
                id__in=selected_skill_ids
            )

            total_required_skills = required_skills.count()
            matched_skills_count = matched_skills.count()

            if total_required_skills > 0:
                score = round(
                    (matched_skills_count / total_required_skills) * 100
                )
            else:
                score = 0

            context.update({
                "selected_role": selected_role,
                "selected_skill_ids": selected_skill_ids,
                "selected_skills": selected_skills,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "total_required_skills": total_required_skills,
                "matched_skills_count": matched_skills_count,
                "score": score,
            })

    return render(request, "myapp/home.html", context)