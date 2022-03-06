from os.path import splitext

from django.forms import FileField

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
