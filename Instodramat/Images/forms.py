from django.forms import ModelForm
from .models import Photo, Comment
from django import forms
from PIL import Image
from django.core.files.storage import default_storage as storage


def prevent_rotate_flag(image):
    """
    Image.open() method reads ExifTags, and there is flag created when picture is taken.
    This flag contain integer from 0 to 8 which stands for rotation of camera.
    It is necessary to check this flag and rotate image.
    """
    # If there is no exiftags just return picture
    try:
        exif = image._getexif()  # Check exif
        image_orientation = exif[274]  # Get orientation flag
        if image_orientation in (2,'2'):
            return image.transpose(Image.FLIP_LEFT_RIGHT)
        elif image_orientation in (3,'3'):
            return image.transpose(Image.ROTATE_180)
        elif image_orientation in (4,'4'):
            return image.transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (5,'5'):
            return image.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (6,'6'):
            return image.transpose(Image.ROTATE_270)
        elif image_orientation in (7,'7'):
            return image.transpose(Image.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (8,'8'):
            return image.transpose(Image.ROTATE_90)
        else:
            return image
    except (AttributeError, IndexError, TypeError):
        return image


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
        image = prevent_rotate_flag(image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((1080, 1080))

        # Some magic to save photo in dropbox
        fh = storage.open(photo.primaryphoto.name, "w")
        picture_format = 'jpg'
        resized_image.save(fh, picture_format)
        fh.close()
        resized_image.save(photo.image.path)
        return photo


class CommentAddForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text_content',)


class EditPhotoForm(ModelForm):

    class Meta:
        model = Photo
        fields = ('text_content',)
