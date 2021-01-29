from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileCreationForm, EmailUserCreationForm
from .models import Profile
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core import serializers


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
        self.photos = user.photos.all()
        return user

    # Add profile object to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        context['photos'] = self.photos
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
            profileform = ProfileCreationForm(request.POST, request.FILES)
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

@login_required(login_url='/login')
def follow_ajax(request, pk):
    # Check if request is ajax
    if request.is_ajax and request.method == "GET":
        # Get all required data
        followed_user = User.objects.get(pk=pk)
        user_profile = request.user.profile  # Get related profile from OneToOne field
        if followed_user not in user_profile.follow.all():
            user_profile.follow.add(followed_user)
            return JsonResponse({
                'message': 'User has been successful followed',
                'follow_status': True}, status=200)
        else:
            user_profile.follow.remove(followed_user)
            return JsonResponse({
                'message': 'Photo has been successful unfollowed',
                'follow_status': False}, status=200)
    else:
        return JsonResponse({'message': 'Wrong method for user following or request not AJAX'}, status=400)


@login_required(login_url='/login')
def followers_list_ajax(request, pk):
    """
    Get list of users that follow you. Response as JSON
    """
    if request.is_ajax and request.method == "GET":
        user = User.objects.get(pk=pk)
        followers = user.profile.followers.all()
        users_json = serializers.serialize('json', followers)
        return HttpResponse(users_json)
    else:
        return JsonResponse({'message': 'Wrong method for getting list or request not AJAX'}, status=400)

@login_required(login_url='/login')
def follow_list_ajax(request, pk):
    """
    Get list of users that you are following. Response as JSON
    """
    if request.is_ajax and request.method == "GET":
        user = User.objects.get(pk=pk)
        follow = user.profile.follow.all()
        users_json = {
            'meta': {
                'title': 'List of people that you follow' # List of your followers
            },
            'data': {}
        }
        for index, followed_user in enumerate(follow):
            data = {
                'username': followed_user.username,
                'user_pk': followed_user.pk,
                'first_name': followed_user.profile.first_name,
                'last_name': followed_user.profile.last_name,
                'profile_pk': followed_user.profile.pk,
                'avatar_url': followed_user.profile.get_avatar()
            }
            users_json['data'][index] = data
        return JsonResponse(users_json)
    else:
        return JsonResponse({'message': 'Wrong method for getting list or request not AJAX'}, status=400)









