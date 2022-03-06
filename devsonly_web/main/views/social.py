from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from src.logger import init_logger
from src.social import filetype
from main.models import Post, PostMedia
from main.forms.social import PostForm

from main.models import User, HardSkills, UserSkills
from main.forms.social import SkillsForm


def index_page(request) -> None:

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(type(ip))

    return render(request, 'pages/index.html')


@login_required
def add_post_page(request) -> None:
    context = {}
    logger = init_logger(__name__)

    if request.method == 'POST':
        post_form = PostForm(request.POST,
                             request.FILES)
        if post_form.is_valid():
            cd = post_form.cleaned_data
            images = []
            audios = []
            videos = []
            files = []

            post = Post(text=cd['text'],
                        author=request.user,
                        created=datetime.today(),
                        modified=datetime.today(),
                        comment_type=cd['comment_type'],
                        likes=0,
                        dislikes=0)
            post.save()

            messages.success(request,
                             'Successfully saved.')
            logger.info('Post has been successfully saved.')

            # Saving media
            for file in request.FILES.getlist('file'):
                if filetype(file) == 'image':
                    media = PostMedia(post=post,
                                      image=file)
                    media.save()
                    images.append({'file': media.image,
                                   'name': file})
                elif filetype(file) == 'audio':
                    media = PostMedia(post=post,
                                      audio=file)
                    media.save()
                    audios.append({'file': media.audio,
                                   'name': file})
                elif filetype(file) == 'video':
                    media = PostMedia(post=post,
                                      video=file)
                    media.save()
                    videos.append({'file': media.video,
                                   'name': file})
                else:
                    media = PostMedia(post=post,
                                      file=file)
                    media.save()
                    files.append({'file': media.file,
                                  'name': file})

            context.update({'post': post,
                            'images': images,
                            'audios': audios,
                            'videos': videos,
                            'files': files,
                            })
        else:
            logger.error('Unable to save post.')
    else:
        post_form = PostForm()

    context.update({'pagename': 'Add post',
                    'post_form': post_form,
                    })
    return render(request, 'pages/add_post.html', context)


def users_page(request) -> None:
    context = {}
    skills_form = SkillsForm(request.GET)
    skills = []
    skill_ids = []
    users = []
    user_ids = []

    # Collecting existing skill tags
    for skill in HardSkills.objects.all():
        skills.append(skill.tag)
    print(skills)

    if skills_form.is_valid():
        requested_skills = skills_form.cleaned_data['requested_skills'].split()
        for skill in requested_skills:
            skill_ids.append(HardSkills.objects.get(tag=skill).id)

        user_ids = UserSkills.objects.filter(skill_id__in=skill_ids)
        user_ids = list(user_ids.values_list('user_id', flat=True).distinct())
        for user_id in user_ids:
            if not all(UserSkills.objects.filter(skill_id=skill_id).exists() for skill_id in skill_ids):
                user_ids.remove(user_id)
        users = User.objects.filter(id__in=user_ids)
        context.update({'users': users})

    context.update({'pagename': 'Users',
                    'skills_form': skills_form,
                    'skills': skills
                    })
    return render(request, 'pages/users.html', context)
