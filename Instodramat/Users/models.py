from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from Scripts.RenamePath import RenamePath
from os import remove
from . import default_vars


class Profile(models.Model):
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    birthday = models.DateField(blank=True, null=True) # in future will be required
    description = models.CharField(max_length=255, blank=True, null=True)
    rename_path = RenamePath('Avatars')  # Create object from Scripts.RenamePath to rename uploaded avatar
    avatar = models.ImageField(upload_to=rename_path, blank=True, null=True)
    # Related with specific user one to one
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Users can decide if they want to display their nicknames in profile or first and last name
    DISPLAY_NAME_CHOICE_VALUES = (
        (True, "Full name"),
        (False, "Only username"),
    )
    display_name = models.BooleanField(choices=DISPLAY_NAME_CHOICE_VALUES, blank=False, null=False)
    # Relation for associate followers
    follow = models.ManyToManyField(User, related_name='followers')
    GENDER_CHOICE_VALUES = (
        ('Male', "Male"),
        ('Female', "Female"),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE_VALUES, blank=False, null=False)

    def delete(self, using=None, keep_parents=False):
        # Check if user is using default avatar
        if self.avatar:
            remove(settings.MEDIA_ROOT + "/" + self.avatar.name)
        super().delete()

    def get_name_to_display(self):
        return f'{self.first_name} {self.last_name}' if self.display_name else self.user.username

    def get_avatar(self):
        return self.avatar.url if self.avatar.name else default_vars.DEFAULT_AVATAR

