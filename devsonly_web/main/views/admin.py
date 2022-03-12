from datetime import date, timedelta

from django.shortcuts import render
from django.contrib import messages

from src.logger import init_logger
from main.models import User


def index_page(request) -> None:

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(type(ip))

    return render(request, 'pages/index.html')


def userlist_page(request) -> None:
    context = {}
    logger = init_logger(__name__)

    if request.method == 'POST':
        if 'moder toggle' in request.POST:
            user = User.objects.get(id=request.POST['moder toggle'])
            user.is_moder = not user.is_moder
            user.save()
        if 'staff toggle' in request.POST:
            user = User.objects.get(id=request.POST['staff toggle'])
            user.is_staff = not user.is_staff
            user.save()
        if 'warning' in request.POST:
            user = User.objects.get(id=request.POST['warning'])
            user.nwarns += 1
            if user.nwarns >= 3:
                user.is_banned = True
            user.save()
        if 'ban toggle' in request.POST:
            user = User.objects.get(id=request.POST['ban toggle'])
            user.is_banned = not user.is_banned
            user.nwarns = 0
            if user.is_banned:
                user.unban_date = date.today() + timedelta(days=30)
            else:
                user.unban_date = None
                user.permanent_ban = False
            user.save()
        if 'permaban' in request.POST:
            user = User.objects.get(id=request.POST['permaban'])
            user.is_banned = True
            user.nwarns = 0
            user.permanent_ban = True
            user.save()

    if request.user.is_superuser or request.user.is_staff:
        users = User.objects.all()
        context.update({
            'users': users
        })
    else:
        messages.add_message(request, messages.ERROR, 'You do not have the permissions to view this page')

    return render(request, 'pages/userlist.html', context)
