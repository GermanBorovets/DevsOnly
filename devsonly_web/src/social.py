from os.path import splitext

from django.forms import FileField

from main.models import Post, PostMedia


def filetype(file: FileField) -> str:
    # Returns file type by its extension
    image_extensions = ['.jpeg',
                        '.jpg',
                        '.png',
                        '.gif',
                        '.bmp',
                        ]
    audio_extensions = ['.mp3',
                        '.flac',
                        '.wav',
                        '.aac',
                        ]
    video_extensions = ['.mp4',
                        '.ogg',
                        '.avi',
                        '.mkv',
                        ]
    ext = splitext(file.name)[1].lower()

    if ext in image_extensions:
        return 'image'
    elif ext in audio_extensions:
        return 'audio'
    elif ext in video_extensions:
        return 'video'
    else:
        return 'file'


def filename(file: FileField) -> str:
    # Returns file name without path
    path = file.name
    return path[path.rfind('/') + 1:]


def collect_postfiles(request, field, post: Post) -> dict:
    # Collects post files from field in request.FILES
    images = []
    audios = []
    videos = []
    files = []
    for file in request.FILES.getlist(field):
        if filetype(file) == 'image':
            media = PostMedia(post=post,
                              image=file)
            media.save()
            images.append({'file': media.image,
                           'name': filename(media.image)})
        elif filetype(file) == 'audio':
            media = PostMedia(post=post,
                              audio=file)
            media.save()
            audios.append({'file': media.audio,
                           'name': filename(media.audio)})
        elif filetype(file) == 'video':
            media = PostMedia(post=post,
                              video=file)
            media.save()
            videos.append({'file': media.video,
                           'name': filename(media.video)})
        else:
            media = PostMedia(post=post,
                              file=file)
            media.save()
            files.append({'file': media.file,
                          'name': filename(media.file)})

        return {'images': images,
                'audios': audios,
                'videos': videos,
                'files': files}
