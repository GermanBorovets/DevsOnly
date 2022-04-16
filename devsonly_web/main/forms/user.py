from django import forms
from django.core.exceptions import ValidationError

from src.registration import validate_letters, validate_password, validate_birth_date
from main.models import User


class ProfileForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=16,
                               required=False)
    profile_picture = forms.ImageField(label='Change profile picture',
                                       required=False)
    status = forms.CharField(label='Status',
                             required=False)
    first_name = forms.CharField(label='First name',
                                 max_length=24,
                                 validators=[validate_letters],
                                 required=False)
    last_name = forms.CharField(label='Last name',
                                max_length=24,
                                validators=[validate_letters],
                                required=False)
    date_of_birth = forms.DateField(label='Date of birth',
                                    widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY'}),
                                    input_formats=['%d-%m-%Y'],
                                    validators=[validate_birth_date],
                                    required=False)
    subjective = forms.CharField(label='Subjective',
                                 max_length=16,
                                 widget=forms.TextInput(attrs={'placeholder': 'they',
                                                               'class': 'form-control'}),
                                 validators=[validate_letters],
                                 required=False)
    objective = forms.CharField(label='Objective',
                                max_length=16,
                                widget=forms.TextInput(attrs={'placeholder': 'them',
                                                              'class': 'form-control'}),
                                validators=[validate_letters],
                                required=False)
    education = forms.CharField(label='Education',
                                max_length=32,
                                required=False)
    work_place = forms.CharField(label='Work place',
                                 max_length=32,
                                 required=False)

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']

        if username != self.initial['initial_username'] and User.objects.filter(username=username).exists():
            raise ValidationError('This username is already used.',
                                  code='used username')

        if all(char.isdigit() for char in username):
            raise ValidationError('Username must not consist only of digits.',
                                  code='invalid username')
        return username


class EmailForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']

        if email == self.initial['initial_email']:
            raise ValidationError('You are already using this email.',
                                  code='initial email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already used.',
                                  code='used email')
        return email


class PasswordForm(forms.Form):
    old_password = forms.CharField(label='Old password',
                                      max_length=24,
                                      widget=forms.PasswordInput)
    new_password = forms.CharField(label='New password',
                               max_length=24,
                               widget=forms.PasswordInput,
                               validators=[validate_password])

    def clean_old_password(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')

        if not self.initial['user'].check_password(old_password):
            raise ValidationError('Invalid old password',
                                  code='invalid old password')
        return old_password

    def clean(self):
        cleaned_data=super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')

        if new_password and new_password == old_password:
            self.add_error(new_password,
                           ValidationError('New password is the same.',
                                           code='same password'))


class SkillsForm(forms.Form):
    requested_skills = forms.CharField(widget=forms.HiddenInput,
                                       required=False)
