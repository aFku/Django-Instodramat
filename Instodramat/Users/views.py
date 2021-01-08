from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileCreationForm, EmailUserCreationForm
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

# -----------------------------------------------------------------------------------------------------------------

def user_create_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            userform = EmailUserCreationForm(request.POST)
            profileform = ProfileCreationForm(request.POST)
            if userform.is_valid() and profileform.is_valid():
                # Create here two objects, and connect them.
                new_user = userform.save()
                # Create profile
                new_profile = profileform.save()
                # Connect user with profile with one to one field
                new_profile.user = new_user
                new_profile.save()
                messages.success(request, 'Account has been created successfully')
                return redirect(f'profile/{new_user.id}')
            else:
                messages.error(request, 'Account cannot be created')
        else:
            userform = EmailUserCreationForm()
            profileform = ProfileCreationForm()
        return render(request, 'registry.html', {'user_form': userform, 'profile_form': profileform})
    #### For a moment
    return HttpResponseNotFound('temporary redirection')




