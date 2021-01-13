from django.forms import ModelForm
from .models import Photo
from django import forms
from PIL import Image


class AddPhotoForm(ModelForm):
    """
    Form for adding photos but with jquery cropper.
    """

    class Meta:
        model = Photo
        fields = ('text_content', 'image')
        labels = {
            'text_content': 'Description',
            'image': 'Photo',
        }
