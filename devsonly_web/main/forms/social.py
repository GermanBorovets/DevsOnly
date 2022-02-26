from django import forms


class SkillsForm(forms.Form):
    requested_skills = forms.CharField(widget=forms.HiddenInput)
