from django import forms
from .models import comment_data


class comment_form(forms.ModelForm):
    class Meta:
        model = comment_data
        fields = ['body']
