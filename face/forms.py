
from django import forms


class UploadImageForm(forms.Form):
    title = forms.CharField(max_length=50)
    image = forms.ImageField()

class FaceLoginForm(forms.Form):
    image = forms.ImageField()
