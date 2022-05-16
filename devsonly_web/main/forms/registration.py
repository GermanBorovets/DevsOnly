from django import forms
from django.core.exceptions import ValidationError

from src.registration import (validate_letters, validate_username,
                              validate_email, validate_password,
                              validate_birth_date)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=16,
                               validators=[validate_username])
    email = forms.EmailField(label='Email',
                             validators=[validate_email])
    password = forms.CharField(label='Password',
                               max_length=24,
                               widget=forms.PasswordInput,
                               validators=[validate_password])
    double_password = forms.CharField(label='Repeat password',
                                      max_length=24,
                                      widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name',
                                 max_length=24,
                                 validators=[validate_letters],
                                 required=False)
    last_name = forms.CharField(label='Last name',
                                max_length=24,
                                validators=[validate_letters],
                                required=False)
    date_of_birth = forms.DateField(label='Date of birth',
                                    widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YY'}),
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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        double_password = cleaned_data.get('double_password')

        if password and password != double_password:
            self.add_error('password',
                           ValidationError('Passwords do not match.',
                                           code='no match'))


class Login(forms.Form):
    username = forms.CharField(max_length=255,
                               label='Username')
    password = forms.CharField(max_length=255,
                               widget=forms.PasswordInput,
                               label='Password')
