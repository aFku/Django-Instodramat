from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .models import Profile


class ProfileView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'profile.html'

    # Find user and profile and photos
    def get_object(self):
        # Get user
        user = get_object_or_404(User, id=self.kwargs['pk'])
        # If user exist find profile (and add this in get_context_data)
        self.profile = get_object_or_404(Profile, user=user)
        # Get all user's photos related by their FK with related_name = photos
        #self.photos = user.photos.all()
        return user

    # Add profile object to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        #context['photos'] = self.photos
        return context
