from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
#from ..Scripts.RenamePath import RenamePath
from os import remove
#import default_vars


class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birthday = models.DateField()
    description = models.CharField(max_length=255)
#    rename_path = RenamePath('Avatars')  # Create object from Scripts.RenamePath to rename uploaded avatar
    avatar = models.ImageField(upload_to='rename_path', blank=True, null=False, default='default_vars.DEFAULT_AVATAR')
    # Related with specific user one to one
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Users can decide if they want to display their nicknames in profile or first and last name
    DISPLAY_NAME_CHOICE_VALUES = (
        (f'{first_name} {last_name}', "Full name"),
        (user.name, "Only username"),
    )
    display_name = models.CharField(max_length=71, choices=DISPLAY_NAME_CHOICE_VALUES)
    # Relation for associate followers
    follow = models.ManyToManyField(User, related_name='followers')
    GENDER_CHOICE_VALUES = (
        ('Male', "Male"),
        ('Female', "Female"),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE_VALUES)

    def delete(self, using=None, keep_parents=False):
        # Check if user is using default avatar
        if self.avatar.name != default_vars.DEFAULT_AVATAR:
            remove(settings.MEDIA_ROOT + "/" + self.avatar.name)
        super().delete()
