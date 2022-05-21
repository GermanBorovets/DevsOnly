from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from main.models import PostMedia


class PostForm(forms.Form):
    """! PostForm class
    """
    text = forms.CharField(label='Text',
                           widget=forms.TextInput(attrs={'placeholder': 'Write your text here...'}),
                           required=False)
    file = forms.FileField(label='Upload file',
                           widget=forms.ClearableFileInput(attrs={'multiple': True}),
                           required=False)
    comment_type = forms.ChoiceField(label='Comments type',
                                     choices=[(0, 'Anonymous'),
                                              (1, 'Not Anonymous')])

    def clean(self) -> None:
        cd = super().clean()
        block_fields = [cd.get('text'),
                        cd.get('image'),
                        cd.get('audio'),
                        cd.get('video'),
                        cd.get('file')]
        if all(field is None or field == '' for field in block_fields):
            raise ValidationError('Block can not be empty',
                                  code='empty block')


class SkillsForm(forms.Form):
    """! SkillsForm class
    """
    requested_skills = forms.CharField(widget=forms.HiddenInput)


class CommentForm(forms.Form):
    """! CommentForm class
    """
    text = forms.CharField(label='Text',
                           widget=forms.TextInput(attrs={'placeholder': 'Write here...'}),
                           required=False)
    file = forms.FileField(label='Upload file',
                           widget=forms.ClearableFileInput(attrs={'multiple': True}),
                           required=False)

    def clean(self):
        cd = super().clean()
        text = cd.get('text')
        file = cd.get('file')
        if text == '' and file is None:
            raise ValidationError('You can not save empty comment',
                                  code='empty')


class EditPostForm(forms.Form):
    """! EditPostForm class
    """
    text = forms.CharField(label='Change text',
                           required=False)
    new_media = forms.FileField(label='Add file',
                                widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                required=False)
    deleted_media = forms.CharField(widget=forms.HiddenInput,
                                    required=False)

    def clean_deleted_media(self) -> forms.CharField:
        cleaned_data = super().clean()
        deleted_media = cleaned_data.get('deleted_media').split()
        for dm in deleted_media:
            if not PostMedia.objects.filter(Q(image=dm) |
                                            Q(audio=dm) |
                                            Q(video=dm) |
                                            Q(file=dm)).exists():
                raise ValidationError('Invalid value',
                                      code='invalid')
        return deleted_media
