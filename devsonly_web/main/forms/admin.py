from django import forms


class BanTimeForm(forms.Form):
    BanSeconds = forms.IntegerField(required=False)


class MuteTimeForm(forms.Form):
    MuteSeconds = forms.IntegerField(required=False)
