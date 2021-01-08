from .models import Profile
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date


# To remember (for me ofc :D ): When form.add_error(None, error) - error added as non_field


class DateInput(forms.DateInput):
    """
    Date insted of text
    """
    input_type = 'date'


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
        # Set min value of birthday to 1990 and max to current date.
        # It will be impossible to choose date out of this range in date picker.
        widgets = {
            'description': forms.Textarea(),
            'birthday': DateInput(attrs={'min': '1990-01-01', 'max': date.today()}),
        }

    def clean(self):
        cleaned_data = super(ProfileCreationForm, self).clean()
        # Check if both name fields are empty
        empty_name = True if cleaned_data.get('first_name') is None and cleaned_data.get('last_name') is None else False
        # If name fields are empty and user want to display full name form is not valid
        if empty_name and cleaned_data.get('display_name'):
            self.add_error('display_name', 'Wrong choice')  # Error for field
            self.add_error(None, ValidationError('You cannot choose full name to be '
                                                 'displayed while you leave name fields empty'))  # Error for form


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
