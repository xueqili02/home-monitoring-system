
from django import forms


class UploadImageForm(forms.Form):
    image = forms.ImageField()

class FaceLoginForm(forms.Form):
    image = forms.ImageField()
