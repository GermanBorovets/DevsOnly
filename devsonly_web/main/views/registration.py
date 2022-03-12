from datetime import date

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from main.forms.registration import RegistrationForm, Login
from main.models import User, UserSettings
from src.common import get_ip
from src.logger import init_logger


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


def login_page(request) -> None:
    context = {
        'pagename': 'Authorization'
    }
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_banned:
                    if date.today() < user.unban_date or user.permanent_ban:
                        messages.add_message(request,
                                             messages.ERROR,
                                             "You are banned")
                    else:
                        user.nwarns = 0
                        user.is_banned = False
                        user.unban_date = None
                        user.save()

                if not user.is_banned:  # not using "else" to avoid login repetition
                    login(request, user)
                    HttpResponseRedirect('/')
                    messages.add_message(request,
                                         messages.SUCCESS,
                                         "Login succesful")
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     "Wrong username or password")
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 "Invalid data")
    else:
        form = Login()
    context.update({
        'form': form,
    })
    return render(request, 'pages/login.html', context)
