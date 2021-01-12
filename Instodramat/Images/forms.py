from django.forms import ModelForm
from models import Photo


class AddPhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ('text_content', 'image')
        lables = {
            'text_content': 'Description',
            'image': 'Photo',
        }
