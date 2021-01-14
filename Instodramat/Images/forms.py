from django.forms import ModelForm
from .models import Photo
from django import forms
from PIL import Image


class AddPhotoForm(ModelForm):
    """
    Form for adding photos but with jquery cropper.
    """

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('text_content', 'image', 'x', 'y', 'width', 'height')
        labels = {
            'text_content': 'Description',
            'image': 'Photo',
        }

    def save(self):
        photo = super(AddPhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400, 400))
        resized_image.save(photo.image.path)

        return photo
