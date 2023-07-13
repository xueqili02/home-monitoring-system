from django import forms

class PLYForm(forms.Form):
    file = forms.FileField()
