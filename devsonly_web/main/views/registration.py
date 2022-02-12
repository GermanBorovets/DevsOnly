from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from main.forms.registration import Login


def login_page(request) -> None:
    context = {}
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                login(request, user)
                HttpResponseRedirect('/')
                messages.add_message(request,
                                     messages.SUCCESS,
                                     "Авторизация успешна")
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     "Неверный логин или пароль")
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 "Неверный формат данных")
    else:
        form = Login()
    context.update({
        'form': form,
    })
    return render(request, 'pages/login.html', context)
