from datetime import datetime, timedelta, date, timezone

from django.shortcuts import render
from django.contrib import messages

from src.logger import init_logger
from src.common import get_ip
from main.models import User, Punishments, BannedIPs


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
            punishment = Punishments(user=user,
                                     type=1,
                                     date=datetime.now().replace(tzinfo=timezone.utc),
                                     executor=request.user)
            punishment.save()
            user.nwarns += 1
            if user.nwarns == 3:
                punishment = Punishments(user=user,
                                         type=0,
                                         date=datetime.now().replace(tzinfo=timezone.utc),
                                         expire_date=datetime.now().replace(tzinfo=timezone.utc) + timedelta(days=30),
                                         executor=request.user
                                         )
                punishment.save()

            user.save()
        if 'ban toggle' in request.POST:
            user = User.objects.get(id=request.POST['ban toggle'])
            if Punishments.objects.filter(user=user, type=0).exists():
                punishment = Punishments.objects.get(user=user, type=0)
                punishment.delete()
            elif Punishments.objects.filter(user=user, type=2).exists():
                punishment = Punishments.objects.get(user=user, type=2)
                punishment.delete()
            else:
                punishment = Punishments(user=user,
                                         type=0,
                                         date=datetime.now().replace(tzinfo=timezone.utc),
                                         expire_date=datetime.now().replace(tzinfo=timezone.utc) + timedelta(days=30),
                                         executor=request.user
                                         )
                punishment.save()
        if 'permaban' in request.POST:
            punishment = Punishments(user=User.objects.get(id=request.POST['ban toggle']),
                                     type=0,
                                     date=datetime.now().replace(tzinfo=timezone.utc),
                                     executor=request.user
                                     )
            punishment.save()
        if 'mute toggle' in request.POST:
            punishment = Punishments(user=User.objects.get(id=request.POST['mute toggle']),
                                     type=3,
                                     date=datetime.now().replace(tzinfo=timezone.utc),
                                     expire_date=datetime.now().replace(tzinfo=timezone.utc) + timedelta(days=30),
                                     executor=request.user
                                     )
            punishment.save()
        if 'delete user' in request.POST:
            user = User.objects.get(id=request.POST['delete user'])
            user.delete()
        if 'ip ban' in request.POST:
            ip = BannedIPs(ip=get_ip(request))
            ip.save()

    if request.user.is_superuser or request.user.is_staff or request.user.is_moder:
        users = User.objects.all()
        punishments = {}
        for i in users:
            if Punishments.objects.filter(user=i, type=0).exists():
                punishments.update({i: True})
            else:
                punishments.update({i: False})
        print(punishments)
        context.update({
            'users': users,
            'punishments': punishments
        })
    else:
        messages.add_message(request, messages.ERROR, 'You do not have the permissions to view this page')

    return render(request, 'pages/userlist.html', context)
