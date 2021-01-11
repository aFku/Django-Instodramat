from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileCreationForm, EmailUserCreationForm
from .models import Profile
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

# -------------------------- Class-based


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


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    # Redirect users already logged in
    redirect_authenticated_user = True

    success_message = 'Logged in'


class CustomLogoutView(LogoutView):
    """
    This view just add message after log out
    """

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'Successfully logged out')
        return response

# -------------------------- Method-based


def user_create_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            userform = EmailUserCreationForm(request.POST)
            profileform = ProfileCreationForm(request.POST)
            if userform.is_valid() and profileform.is_valid():
                # Create here two objects, and connect them.
                # form.save() is not hashing password, so use create_user()
                new_user = User.objects.create_user(username=userform.cleaned_data['username'],
                                                    password=userform.cleaned_data['password1'],
                                                    email=userform.cleaned_data['email'])
                # Create profile
                new_profile = profileform.save()
                # Connect user with profile with one to one field
                new_profile.user = new_user
                new_profile.save()
                messages.success(request, 'Account has been created successfully')
                return redirect('login')
            else:
                messages.error(request, 'Account cannot be created')
        else:
            userform = EmailUserCreationForm()
            profileform = ProfileCreationForm()
        return render(request, 'registry.html', {'user_form': userform, 'profile_form': profileform})
    #### For a moment
    return HttpResponseNotFound('temporary redirection')



