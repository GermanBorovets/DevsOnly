from django import forms


class Login(forms.Form):
    username = forms.CharField(max_length=255,
                               label='Username')
    password = forms.CharField(max_length=255,
                               widget=forms.PasswordInput,
                               label='Password')
