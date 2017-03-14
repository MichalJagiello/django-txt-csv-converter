from django import forms


class UploadFileForm(forms.Form):
    plik = forms.FileField()
