from django.shortcuts import render

from main.models import User


def index_page(request) -> None:

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(type(ip))

    return render(request, 'pages/index.html')


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
