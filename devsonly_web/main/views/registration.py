from datetime import date

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from main.models import User, UserSettings
from main.forms.registration import RegistrationForm
from src.common import get_ip
from src.logger import init_logger


def index_page(request) -> None:

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(type(ip))

    return render(request, 'pages/index.html')


def registration_page(request) -> None:
    logger = init_logger(__name__)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User(reg_ip=get_ip(request),
                        username=cd['username'],
                        email=cd['email'],
                        password=make_password(cd['password']),
                        first_name=cd['first_name'],
                        last_name=cd['last_name'],
                        date_of_birth=cd['date_of_birth'],
                        date_joined=date.today(),
                        )
            user.save()

            user_settings = UserSettings(user=User.objects.get(username=user.username),
                                         sex=f'{cd["subjective"]}/{cd["objective"]}',
                                         )
            user_settings.save()

            logger.info('Successful registration.')
            return redirect('/')
        else:
            for field in form:
                if field.errors:
                    for error in field.errors:
                        messages.error(request, f'{field.label}: {error}')
    else:
        form = RegistrationForm()
    context = {'pagename': 'Registration',
               'form': form,
               }
    return render(request, 'pages/registration.html', context)
