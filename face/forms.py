
from django import forms


class UploadImageForm(forms.Form):
    file = forms.ImageField()
