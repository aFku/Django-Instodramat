from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileCreationForm, EmailUserCreationForm, UserEmailChangeForm, ProfileDataChangeForm, \
    PasswordResetFormEmailValidation
from .models import Profile
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# -------------------------- Class-based


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'profile.html'
    login_url = '/profile/login/'

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


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    """
    This view just add message after log out
    """
    login_url = 'profile/login/'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'Successfully logged out')
        return response


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """
    Custom view for password reset. It gives user message if mail was send. It also uses new password reset form
    with email validation.
    """
    template_name = 'password_reset.html'
    success_message = 'Email with reset link was send to your email'
    form_class = PasswordResetFormEmailValidation
    # reverse is executing before urls are loaded in this case.
    # To fix it I used reverse_lazy
    success_url = reverse_lazy('login')


class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'password_confirm.html'
    success_message = 'Your password has been changed!'
    success_url = reverse_lazy('login')

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
                print('user:', userform.errors)
                print('profile', profileform.errors)
        else:
            userform = EmailUserCreationForm()
            profileform = ProfileCreationForm()
        return render(request, 'registry.html', {'user_form': userform, 'profile_form': profileform})
    #### For a moment
    return HttpResponseNotFound('temporary redirection')


@login_required(login_url='/profile/login/')
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


@login_required(login_url='/profile/login/')
def followers_list_ajax(request, pk):
    """
    Get list of profiles that follow you. Response as JSON
    """
    if request.is_ajax and request.method == "GET":
        user = User.objects.get(pk=pk)
        follow = user.profile.get_followers_list()  # List of profiles
        users_json = {
            'meta': {
                'title': 'List of people that follow you'  # List of your followers
            },
            'data': {}
        }
        for index, followed_profile in enumerate(follow):
            data = {
                'username': followed_profile.user.username,
                'user_pk': followed_profile.user.pk,
                'first_name': followed_profile.first_name,
                'last_name': followed_profile.last_name,
                'profile_pk': followed_profile.pk,
                'avatar_url': followed_profile.get_avatar(),
                'display_name': followed_profile.get_name_to_display()
            }
            users_json['data'][index] = data
        return JsonResponse(users_json)
    else:
        return JsonResponse({'message': 'Wrong method for getting list or request not AJAX'}, status=400)


@login_required(login_url='/profile/login/')
def follow_list_ajax(request, pk):
    """
    Get list of users that you are following. Response as JSON
    """
    if request.is_ajax and request.method == "GET":
        user = User.objects.get(pk=pk)
        follow = user.profile.get_follow_list()  # List of users
        users_json = {
            'meta': {
                'title': 'List of people that you follow'
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
                'avatar_url': followed_user.profile.get_avatar(),
                'display_name': followed_user.profile.get_name_to_display()
            }
            users_json['data'][index] = data
        return JsonResponse(users_json)
    else:
        return JsonResponse({'message': 'Wrong method for getting list or request not AJAX'}, status=400)


@login_required(login_url='/profile/login/')
def profile_settings_view(request):
    """
    - Change password
    - Change email
    - Change profile data
    - Delete your account
    This view doesn't change anything. It just provide forms.
    All changes are made in specialized views.
    """
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, user=user)

    password_form = PasswordChangeForm(user)
    email_form = UserEmailChangeForm()
    profile_form = ProfileCreationForm(instance=profile)

    return render(request, 'profile_settings.html', context={'password_form': password_form,
                                                             'email_form': email_form,
                                                             'profile_form': profile_form,
                                                             'user': user})


@login_required(login_url='/profile/login/')
def profile_settings_change_password(request):
    """
    View that read POST parameters and change password
    """
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.user.pk)
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Password has been changed!')
        else:
            messages.error(request, 'Password has not been changed!')
        return redirect(reverse('profile_settings'))
    else:
        return HttpResponse(status=404)


@login_required(login_url='/profile/login/')
def profile_settings_change_email(request):
    """
    View that read POST parameters and change email
    """
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.user.pk)
        email_form = UserEmailChangeForm(request.POST, instance=user)
        if email_form.is_valid():
            email_form.save()
            messages.success(request, 'Email has been changed!')
        else:
            messages.error(request, 'Email has not been changed!')
        return redirect(reverse('profile_settings'))
    else:
        return HttpResponse(status=404)


@login_required(login_url='/profile/login/')
def profile_settings_change_profile(request):
    """
    View that read POST parameters and change profile data
    """
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.user.pk)
        profile = get_object_or_404(Profile, user=user)
        profile_form = ProfileDataChangeForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile has been changed!')
        else:
            messages.error(request, 'Profile has not been changed!')
        return redirect(reverse('profile_settings'))
    else:
        return HttpResponse(status=404)


@login_required(login_url='/profile/login/')
def profile_settings_delete_profile(request):
    """
    Delete profile if given password is correct
    """
    if request.method == "POST":
        if request.user.check_password(request.POST.get('delete_password', '')):
            user = get_object_or_404(User, pk=request.user.pk)
            profile = get_object_or_404(Profile, user=user)
            # Delete user
            profile.delete()
            user.delete()
            messages.success(request, 'Account has been deleted!')
            return redirect(reverse('main_page'))
        else:
            messages.error(request, 'Password for delete confirmation is incorrect')
            return redirect(reverse('profile_settings'))
    else:
        return HttpResponse(status=404)
