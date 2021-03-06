from os.path import splitext
from main.models import Post
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


def post_exists(id: int) -> bool:
    return Post.objects.filter(id=id).exists()


def collect_files(request, field, post: Post) -> dict:
    # Collects post files from field in request.FILES
    images = []
    audios = []
    videos = []
    files = []
    for file in request.FILES.getlist(field):
        if filetype(file) == 'image':
            media = PostMedia(post=post,
                              image=file)
            images.append({'file': media.image,
                           'name': filename(media.image)})
        elif filetype(file) == 'audio':
            media = PostMedia(post=post,
                              audio=file)
            audios.append({'file': media.audio,
                           'name': filename(media.audio)})
        elif filetype(file) == 'video':
            media = PostMedia(post=post,
                              video=file)
            videos.append({'file': media.video,
                           'name': filename(media.video)})
        else:
            media = PostMedia(post=post,
                              file=file)
            files.append({'file': media.file,
                          'name': filename(media.file)})
        media.save()
        return {'images': images,
                'audios': audios,
                'videos': videos,
                'files': files}
