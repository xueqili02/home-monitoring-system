
from django import forms


class UploadImageForm(forms.Form):
    file = forms.ImageField()

class FaceLoginForm(forms.Form):
    image = forms.ImageField()
