from .models import Profile
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'avatar', 'description', 'birthday', 'display_name', 'gender')
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'birthday': 'Your birthday',
            'description': 'Profile description',
            'avatar': 'Profile avatar',
            'display_name': 'Choose which name should be displayed in your profile',
            'gender': 'Gender',
        }
        widgets = {
            'description': forms.Textarea(),
        }


class EmailUserCreationForm(UserCreationForm):
    """
    Extended UserCreationForm with Email field
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'password1': '''Passwords must be the same
            - Only letters and digits
            - Password cannot be too popular'''
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

