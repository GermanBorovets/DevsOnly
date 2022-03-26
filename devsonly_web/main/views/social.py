from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.contrib import messages

from src.logger import init_logger
from src.social import filetype, filename, collect_files
from main.models import Post, PostMedia, User, HardSkills, UserSkills
from main.forms.social import PostForm, SkillsForm, EditPostForm


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
            media = collect_files(request,
                                      'file',
                                      post)

            context.update({'post': post,
                            'images': media.get('images'),
                            'audios': media.get('audios'),
                            'videos': media.get('videos'),
                            'files': media.get('files'),
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


@login_required
def edit_post_page(request, post_id):
    context = {}
    logger = init_logger(__name__)
    try:
        post = Post.objects.get(id=post_id)
    except:
        raise Http404
    if post.author == request.user:
        images = []
        audios = []
        videos = []
        files = []
        if request.method == 'POST':
            edit_form = EditPostForm(request.POST,
                                     request.FILES)
            if edit_form.is_valid():
                cd = edit_form.cleaned_data
                post.text = cd['text']
                post.save()

                # Deleting unwanted media
                deleted_media = cd['deleted_media']
                for dm in deleted_media:
                    type = dm[dm.find('/') + 1]
                    if type == 'i':
                        PostMedia.objects.get(post_id=post_id,
                                              image=dm).delete()
                    if type == 'a':
                        PostMedia.objects.get(post_id=post_id,
                                              audio=dm).delete()
                    if type == 'v':
                        PostMedia.objects.get(post_id=post_id,
                                              video=dm).delete()
                    if type == 'f':
                        PostMedia.objects.get(post_id=post_id,
                                              file=dm).delete()

                # Saving added media
                print(edit_form.cleaned_data['deleted_media'])
                new_media = collect_files(request,
                                              'new_media',
                                              post)

        # Collecting current media
        media = PostMedia.objects.filter(post_id=post_id)
        for file in media:
            if file.image:
                images.append({'file': file.image,
                               'name': filename(file.image)})
            if file.audio:
                audios.append({'file': file.audio,
                               'name': filename(file.audio)})
            if file.video:
                videos.append({'file': file.video,
                               'name': filename(file.video)})
            if file.file:
                files.append({'file': file.file,
                              'name': filename(file.file)})

            messages.success(request,
                             'Successfully changed.')
        else:
            edit_form = EditPostForm()

        context.update({'post': post,
                        'images': images,
                        'audios': audios,
                        'videos': videos,
                        'files': files,
                        'edit_form': edit_form
                        })
    else:
        raise Http404
    context.update({'pagename': 'Edit',
                    })
    return render(request, 'pages/edit_post.html', context)
