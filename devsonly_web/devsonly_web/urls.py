"""devsonly_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main.views.index import index_page
from main.views.registration import login_page, registration_page
from main.views.social import show_post_page, add_post_page, users_page
from main.views.social import add_post_page, users_page, edit_post_page
from main.views.user import author_rating_page, team_member_rating_page
from main.views.user import profile_page
from main.views.registration import registration_page, login_page
from main.views.registration import registration_page
from main.views.social import *
from main.views.user import profile_page, edit_profile_page
from main.views.admin import userlist_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('registration/',
         registration_page,
         name='registration'),
    path('login/',
         login_page,
         name='login'),
    path('post/add/',
         author_rating_page,
         name='author_rating'),
    path('rating/member/',
         team_member_rating_page,
         name='team_member_rating'),
    path('users/list/',
         users_page,
         name='users'),
    path('post/<int:post_id>/',
         show_post_page,
         name='show_post'),
    path('profile/',
         profile_page,
         name='profile'),
    path('edit_profile/<int:user_id>/',
         edit_profile_page,
         name='edit_profile'),
    path('login/',
        login_page,
        name='login'),
    path('post/edit/<int:post_id>/',
         edit_post_page,
         name='edit_post'),
    path('userlist/',
         userlist_page,
         name='userlist'),
    ]+static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
