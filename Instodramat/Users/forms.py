from .models import Profile
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from PIL import Image
from django.core.files.storage import default_storage as storage


# To remember (for me ofc :D ): When form.add_error(None, error) - error added as non_field


class DateInput(forms.DateInput):
    """
    Date insted of text
    """
    input_type = 'date'


class ProfileCreationForm(ModelForm):

    # Fields for cropping|They are not required to let user create account without avatars and give them default avatar
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    photo_added = False

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'avatar', 'description', 'birthday', 'display_name',
                  'gender', 'x', 'y', 'width', 'height')
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'birthday': 'Your birthday',
            'description': 'Profile description',
            'avatar': 'Profile avatar',
            'display_name': 'Choose which name should be displayed in your profile',
            'gender': 'Gender',
        }
        # Set min value of birthday to 1990 and max to current date.
        # It will be impossible to choose date out of this range in date picker.
        widgets = {
            'description': forms.Textarea(),
            'birthday': DateInput(attrs={'min': '1990-01-01', 'max': date.today()}),
            'avatar': forms.FileInput(attrs={'id': 'id_image'})  # Just changing id to fit execute_cropper.js
        }

    def clean(self):

        # Remove old photo if exist for updating profile or leave when profile is just created
        # Only here you can reach path for previous avatar
        if self.instance:
            self.instance.remove_avatar()

        cleaned_data = super(ProfileCreationForm, self).clean()
        # Check if both name fields are empty
        empty_name = True if cleaned_data.get('first_name') is None and cleaned_data.get('last_name') is None else False
        # If name fields are empty and user want to display full name form is not valid
        if empty_name and cleaned_data.get('display_name'):
            self.add_error('display_name', 'Wrong choice')  # Error for field
            self.add_error(None, ValidationError('You cannot choose full name to be '
                                                 'displayed while you leave name fields empty'))  # Error for form
        # Check if user added photo
        if cleaned_data.get('avatar'):
            self.photo_added = True

    #cropping when saving
    def save(self):

        profile = super(ProfileCreationForm, self).save()

        # if photo was added or changed fill positions for cropper
        if self.photo_added or 'avatar' in self.changed_data:

            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            image = Image.open(profile.avatar)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((400, 400))

            # Some magic to save photo in dropbox
            fh = storage.open(profile.primaryphoto.name, "w")
            picture_format = 'jpg'
            resized_image.save(fh, picture_format)
            fh.close()
            resized_image.save(profile.image.path)

        return profile


class EmailUserCreationForm(UserCreationForm):
    """
    Extended UserCreationForm with Email field
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super(EmailUserCreationForm, self).clean()
        # Add form errors when form is invalid
        if self.has_error('password2') or self.has_error('password1'):
            self.add_error(None, ValidationError('Password error'))
        if self.has_error('username'):
            self.add_error(None, ValidationError('Username error'))
        if self.has_error('email'):
            self.add_error(None, ValidationError('Email error'))

    def clean_email(self):
        email = self.cleaned_data['email']
        # Check if email was used before
        if User.objects.filter(email=email):
            self.add_error('email', 'This email address is already in use')
        return email


class UserEmailChangeForm(ModelForm):

    confirm_email = forms.EmailField()

    class Meta:
        model = User
        fields = ('email', 'confirm_email')

    def __init__(self, *args, **kwargs):
        super(UserEmailChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True  # Set this field as required when user want to change email

    def clean(self):
        if self.cleaned_data.get('email') != self.cleaned_data.get('confirm_email'):
            return forms.ValidationError('Email addresses not match!')


class ProfileDataChangeForm(ProfileCreationForm):

    def __init__(self, *args, **kwargs):
        super(ProfileDataChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():  # Set all fields not required now, because we have all information that we want already
            field.required = False


class PasswordResetFormEmailValidation(PasswordResetForm):
    """
    Check if there is account with given email address
    """

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            self.add_error('email', 'There is no account associated with this email address!')
        return email
