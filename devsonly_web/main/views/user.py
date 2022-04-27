from typing import Dict

from django.shortcuts import render
from django.contrib import messages

from src.common import from_get_id
from src.logger import init_logger
from src.user import user_exists, userset_exists, get_accesses, is_userset_owner
from main.models import User, UserSettings
from main.models import User


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
    return render(request, 'pages/team_member_rating.html', context)
