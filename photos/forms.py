from django import forms
from django.db.models import fields

from . import models


class NewPhotoForm(forms.ModelForm):

    class Meta:
        model = models.Photo
        fields = ['image', 'description']