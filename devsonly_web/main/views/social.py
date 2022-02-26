from django.shortcuts import render

from main.models import User, HardSkills, UserSkills
from main.forms.social import SkillsForm


def index_page(request) -> None:

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(type(ip))

    return render(request, 'pages/index.html')


def users_page(request) -> None:
    context = {}
    skills_form = SkillsForm(request.GET)
    skills = []
    skill_ids = []
    users = []
    user_ids = []

    # Collecting existing skill tags
    for skill in HardSkills.objects.all():
        skills.append(skill.tag)

    if skills_form.is_valid():
        requested_skills = skills_form.cleaned_data['requested_skills'].split()
        for skill in requested_skills:
            skill_ids.append(HardSkills.objects.get(tag=skill).id)

        user_ids = UserSkills.objects.filter(skill_id__in=skill_ids)
        user_ids = list(user_ids.values_list('user_id', flat=True).distinct())
        for user_id in user_ids:
            if not all(UserSkills.objects.filter(skill_id=skill_id).exists() for skill_id in skill_ids):
                user_ids.remove(user_id)
        users = User.objects.filter(id__in=user_ids)
        context.update({'users': users})

    context.update({'pagename': 'Users',
                    'skills_form': skills_form,
                    'skills': skills
                    })
    return render(request, 'pages/users.html', context)
