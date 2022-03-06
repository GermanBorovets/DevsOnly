from django import forms
from django.core.exceptions import ValidationError


class PostForm(forms.Form):
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
