from datetime import date, datetime, timedelta, timezone

from django.shortcuts import render
from django.contrib import messages

from src.logger import init_logger
from main.models import User, BannedIPs
from main.forms.admin import BanTimeForm, MuteTimeForm


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
            if user.nwarns == 3:
                user.is_banned = True
            user.save()

        if 'ban toggle' in request.POST:
            user = User.objects.get(id=request.POST['ban toggle'])
            ban_form = BanTimeForm(request.POST)
            if not user.is_banned:
                if ban_form.is_valid():
                    if not user.is_banned:
                        if ban_form.cleaned_data['BanSeconds'] is not None:
                            if ban_form.cleaned_data['BanSeconds'] > 0:
                                user.is_banned = True
                                user.nwarns = 0
                                now = datetime.now(tz=timezone(timedelta(seconds=0)))
                                delta = timedelta(seconds=ban_form.cleaned_data['BanSeconds'])
                                user.unban_date = now + delta
                            elif ban_form.cleaned_data['BanSeconds'] == 0:
                                user.is_banned = True
                                user.nwarns = 0
                            else:
                                messages.error(request, 'The number can not be negative')
                else:
                    messages.error(request, 'Enter valid time')
            else:
                user.is_banned = False
                user.unban_date = None
            context.update({'form': ban_form})
            user.save()

        if 'mute toggle' in request.POST:
            user = User.objects.get(id=request.POST['mute toggle'])
            mute_form = MuteTimeForm(request.POST)
            if not user.is_muted:
                if mute_form.is_valid():
                    if not user.is_muted:
                        if mute_form.cleaned_data['MuteSeconds'] is not None:
                            if mute_form.cleaned_data['MuteSeconds'] > 0:
                                user.is_muted = True
                                now = datetime.now(tz=timezone(timedelta(seconds=0)))
                                delta = timedelta(seconds=mute_form.cleaned_data['MuteSeconds'])
                                user.unmute_date = now + delta
                            elif mute_form.cleaned_data['MuteSeconds'] == 0:
                                user.is_muted = True
                            else:
                                messages.error(request, 'The number can not be negative')
                else:
                    messages.error(request, 'Enter valid time')
            else:
                user.is_muted = False
                user.unmute_date = None
            context.update({'form': mute_form})
            user.save()

        if 'delete' in request.POST:
            user = User.objects.get(id=request.POST['delete'])
            user.delete()

        if 'ip ban' in request.POST:
            user = User.objects.get(id=request.POST['ip ban'])
            ip = BannedIPs(IP=user.reg_ip)
            user.is_banned = True
            user.save()
            ip.save()
        users = User.objects.all()
        context.update({
            'users': users,
            'ban_form': BanTimeForm(),
            'mute_form': MuteTimeForm(),
        })

    elif request.user.is_superuser or request.user.is_staff:
        users = User.objects.all()
        context.update({
            'users': users,
            'ban_form': BanTimeForm(),
            'mute_form': MuteTimeForm(),
        })
    else:
        messages.add_message(request, messages.ERROR, 'You do not have the permissions to view this page')

    return render(request, 'pages/userlist.html', context)
