from datetime import datetime, timedelta, timezone

from django.http import Http404
from django.shortcuts import render
from django.contrib import messages
from src.logger import init_logger
from main.models import Post, PostMedia, Comment, CommentElement
from main.forms.social import SkillsForm, CommentForm
from src.social import filetype, filename, collect_files
from main.forms.social import PostForm, SkillsForm, EditPostForm

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
    if user.is_muted:
        if user.unmute_date is None:
            messages.error(request, f"You are not allowed to post")
        elif datetime.now(tz=timezone(offset=timedelta(hours=0))) < user.unmute_date:
            messages.error(request, f"You are not allowed to post until "
                                    f"{user.unmute_date.strftime('%H:%M:%S %d.%m.%Y')} UTC")
        else:
            user.is_muted = False
            user.unmute_date = None
            user.save()
    else:
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
                        'user': request.user
                        })
    return render(request, 'pages/add_post.html', context)


def users_page(request) -> None:
    context = {}
    skills_form = SkillsForm(request.GET)
    skills = []
    skill_ids = []

    # Collecting existing skill tags
    for skill in HardSkills.objects.all():
        skills.append(skill.tag)

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


def show_post_page(request, post_id):
    context = {}

    if Post.objects.filter(id=post_id).exists():
        post = Post.objects.get(id=post_id)
        media = PostMedia.objects.filter(post_id=post_id)

    return render(request, 'pages/post.html', context)


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
        comments = []

        # Collecting post media
        if request.method == 'POST':
            edit_form = EditPostForm(request.POST,
                                     request.FILES)
            if edit_form.is_valid():
                print(edit_form.fields)
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
        else:
            edit_form = EditPostForm()

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

        # Comment form
        if request.user.is_authenticated:
            if request.method == 'POST':
                comment_form = CommentForm(request.POST,
                                           request.FILES)
                if comment_form.is_valid():
                    cd = comment_form.cleaned_data
                    new_comment = Comment(post_id=post_id,
                                          text=cd.get('text'),
                                          author=request.user,
                                          likes=0,
                                          dislikes=0,
                                          created=datetime.now())
                    new_comment.save()

                    # Collecting media for new comment
                    for file in request.FILES.getlist('file'):
                        if filetype(file) == 'image':
                            element = CommentElement(comment=new_comment,
                                                     image=file)
                        elif filetype(file) == 'audio':
                            element = CommentElement(comment=new_comment,
                                                     audio=file)
                        elif filetype(file) == 'video':
                            element = CommentElement(comment=new_comment,
                                                     video=file)
                        else:
                            element = CommentElement(comment=new_comment,
                                                     file=file)
                        element.save()
            else:
                comment_form = CommentForm()
            context.update({'comment_form': comment_form})

        # Collecting existing comments
        for comment in Comment.objects.filter(post_id=post_id):
            comment_images = []
            comment_audios = []
            comment_videos = []
            comment_files = []
            comments.append({'author': comment.author,
                             'text': comment.text,
                             'likes': comment.likes,
                             'dislikes': comment.dislikes,
                             'created': comment.created
                             })

            for element in CommentElement.objects.filter(comment=comment):
                if element.image:
                    comment_images.append({'file': element.image,
                                           'name': filename(element.image)})
                if element.audio:
                    comment_audios.append({'file': element.audio,
                                           'name': filename(element.audio)})
                if element.video:
                    comment_videos.append({'file': element.video,
                                           'name': filename(element.video)})
                if element.file:
                    comment_files.append({'file': element.file,
                                          'name': filename(element.file)})
            comments[-1].update({'images': comment_images,
                                 'audios': comment_audios,
                                 'videos': comment_videos,
                                 'files': comment_files
                                 })
            messages.success(request,
                             'Successfully changed.')
        else:
            edit_form = EditPostForm()

        context.update({'post': post,
                        'images': images,
                        'audios': audios,
                        'videos': videos,
                        'files': files,
                        'comments': comments,
                        'edit_form': edit_form
                        })
    else:
        raise Http404

    context.update({'pagename': 'Edit', })
    return render(request, 'pages/edit_post.html', context)
