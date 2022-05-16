from typing import Dict

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.shortcuts import render
from django.contrib import messages

from src.common import from_get_id
from src.logger import init_logger
from src.user import user_exists, userset_exists, get_accesses, is_userset_owner
from main.models import User, UserSettings, HardSkills, UserSkills
from main.forms.user import ProfileForm, EmailForm, PasswordForm, SkillsForm


logger = init_logger(__name__)


def profile_page(request) -> None:
    context = {}
    user_id: int = from_get_id(request)

    if userset_exists(user_id):
        user = User.objects.get(id=user_id)
        userset = UserSettings.objects.get(user=user)
        accesses: Dict[str, int] = get_accesses(user)

        user_data = [
            # {
            #     'label': 'First name',
            #     'access': 1,
            #     'data': user.first_name
            # },
            # {
            #     'label': 'Last name',
            #     'access': 1,
            #     'data': user.last_name
            # },
            # {
            #     'label': 'Username',
            #     'access': 1,
            #     'data': user.username
            # },
            {
                'label': 'Date of birth',
                'access': accesses['date_of_birth'],
                'data': user.date_of_birth
            },
            {
                'label': 'Profile picture',
                'access': accesses['profile_picture'],
                'data': userset.profile_picture
            },
            {
                'label': 'Status',
                'access': accesses['status'],
                'data': userset.status
            },
            {
                'label': 'Preposition',
                'access': accesses['sex'],
                'data': userset.sex
            },
            {
                'label': 'Hard skills',
                'access': accesses['hard_skills'],
                'data': userset.hard_skills
            },
            {
                'label': 'Work place',
                'access': accesses['work_place'],
                'data': userset.work_place
            },
            {
                'label': 'Education',
                'access': accesses['education'],
                'data': userset.education
            },
        ]
        context.update({
            'pagename': f'{ user.first_name } { user.last_name }',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'user_data': user_data,
        })

    else:
        messages.add_message(request, messages.ERROR, "This user doesn't exist")
        logger.warning("Requested user doesn't exist")

    return render(request, 'pages/profile.html', context)


def author_rating_page(request):
    context = {
        'pagename': 'Author rating',
        'author_rating': User.objects.all()
    }
    return render(request, 'pages/author_rating.html', context)


def team_member_rating_page(request):
    context = {
        'pagename': 'Member rating',
        'team_member_rating': User.objects.all()
    }
    return render(request, 'pages/author_rating.html', context)


@login_required
def edit_profile_page(request, user_id):
    context = {}

    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
    else:
        user = None

    if UserSettings.objects.filter(user_id=user_id).exists():
        user_settings = UserSettings.objects.get(user_id=user_id)
    else:
        user_settings = None

    if request.user == user:
        profile_form = ProfileForm()
        email_form = EmailForm()
        password_form = PasswordForm()
        skills_form = SkillsForm()

        if user.date_of_birth and user.date_of_birth != '':
            date_of_birth = (str(user.date_of_birth.day) + '-' +
                         str(user.date_of_birth.month) + '-' +
                         str(user.date_of_birth.year))
        else:
            date_of_birth = ''

        user_skills = []
        user_skills_ids = set(UserSkills.objects.filter(user_id=user_id).values_list('skill_id',
                                                                                     flat=True))
        skills = []

        for skill in HardSkills.objects.all():
            skills.append(skill.tag)

        for skill_id in user_skills_ids:
            user_skills.append(HardSkills.objects.get(id=skill_id).tag)

        if request.method == 'POST':

            if 'profile_form' in request.POST:
                profile_form = ProfileForm(request.POST,
                                           request.FILES,
                                           initial={'initial_username': user.username})
                if profile_form.is_valid():
                    cleaned_data = profile_form.cleaned_data
                    if cleaned_data['username'] != '':
                        user.username = cleaned_data['username']
                    if 'profile_picture' in request.FILES:
                        user_settings.profile_picture = cleaned_data['profile_picture']
                    user_settings.status = cleaned_data['status']
                    user.first_name = cleaned_data['first_name']
                    user.last_name = cleaned_data['last_name']
                    if cleaned_data['date_of_birth'] != '':
                        user.date_of_birth = cleaned_data['date_of_birth']
                    user_settings.sex = f"{cleaned_data['subjective']}/{cleaned_data['objective']}"
                    user_settings.education = cleaned_data['education']
                    user_settings.work_place = cleaned_data['work_place']
                    user.save()
                    user_settings.save()
                    messages.success(request,
                                     'Successfully changed profile.')

            if 'email_form' in request.POST:
                email_form = EmailForm(request.POST,
                                       initial={'initial_email': user.email})
                if email_form.is_valid():
                    user.email = email_form.cleaned_data['email']
                    user.save()
                    messages.success(request,
                                     'Successfully changed email.')

            if 'password_form' in request.POST:
                password_form = PasswordForm(request.POST,
                                             initial={'user': user})
                if password_form.is_valid():
                    user.password = make_password(password_form.cleaned_data['new_password'])
                    user.save()
                    if user.is_active:
                        login(request, user)
                    messages.success(request,
                                     'Successfully changed password.')

            if 'skills_form' in request.POST:
                skills_form = SkillsForm(request.POST)
                if skills_form.is_valid():
                    requested_skills = skills_form.cleaned_data['requested_skills'].split()

                    # Delete unwanted skills
                    for skill in UserSkills.objects.filter(user_id=user_id):
                        tag = HardSkills.objects.get(id=skill.skill_id).tag
                        if tag not in requested_skills:
                            skill.delete()
                            user_skills.remove(tag)

                    # Add new user skills
                    for skill in requested_skills:
                        hard_skill = HardSkills.objects.get(tag=skill)
                        if not UserSkills.objects.filter(skill_id=hard_skill.id,
                                                         user_id=user_id).exists():
                            user_skill = UserSkills(skill_id=hard_skill.id,
                                                    user_id=user_id)
                            user_skill.save()
                            user_skills.append(skill)
                    messages.success(request,
                                     'Successfully changed user skills.')
    else:
        raise Http404

    context.update({'pagename': 'Edit profile',
                    'profile_form': profile_form,
                    'email_form': email_form,
                    'password_form': password_form,
                    'skills_form': skills_form,
                    'user': user,
                    'user_settings': user_settings,
                    'user_skills': user_skills,
                    'skills': skills,
                    'date_of_birth': date_of_birth
                    })
    return render(request, 'pages/edit_profile.html', context)
