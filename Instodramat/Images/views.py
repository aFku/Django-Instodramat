from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddPhotoForm, CommentAddForm
from django.contrib import messages
from .models import Photo, Comment
from django.http import JsonResponse


@login_required(login_url='profile/login/')
def add_image_view(request):
    if request.method == "POST":
        photo_form = AddPhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            # Create Photo with data from form and fill author with current user
            photo = photo_form.save()
            photo.author = request.user
            photo.save()
            messages.success(request, 'Photo added')
        else:
            messages.error(request, 'Cannot add new photo')
        return redirect('/')
    else:
        photo_form = AddPhotoForm()
        return render(request, 'add_photo.html', {'form': photo_form})


@login_required(login_url='profile/login/')
def image_preview(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    comments_set = photo.get_comments()
    if request.method == "POST":
        form = CommentAddForm(request.POST)
        if form.is_valid():
            comment = Comment(**form.cleaned_data, author=request.user, related_photo=photo)
            comment.save()
        else:
            messages.error(request, "Comment cannot be added!")
    form = CommentAddForm()
    return render(request, 'photo_preview.html', {'photo': photo, 'form': form, 'comments': comments_set})


@login_required(login_url='profile/login/')
def like_photo_ajax(request, photo_id):
    # check if request is ajax
    if request.is_ajax and request.method == "GET":
        # Get photo to access 'likes' field
        photo = Photo.objects.get(id=photo_id)
        user = request.user
        # User is not liking this photo so view will add this user to likes
        if user not in photo.likes.all():
            photo.likes.add(user)
            return JsonResponse({
                'message': 'Photo has been successful liked',
                'like_status': True}, status=200)
        else:
            photo.likes.remove(user)
            return JsonResponse({
                'message': 'Photo has been successful unliked',
                'like_status': False}, status=200)
    else:
        return JsonResponse({'message': 'Wrong method for liking photo or request not AJAX'}, status=400)


@login_required(login_url='profile/login/')
def get_likes_list_ajax(request, photo_id):
    """
    Get list of users that like this photo. Response as JSON
    """
    if request.is_ajax and request.method == "GET":
        photo = Photo.objects.get(pk=photo_id)
        likes = photo.get_likes_list()
        users_json = {
            'meta': {
                'title': 'List of people that like this photo'
            },
            'data': {}
        }
        for index, liker in enumerate(likes):
            data = {
                'username': liker.username,
                'user_pk': liker.pk,
                'first_name': liker.profile.first_name,
                'last_name': liker.profile.last_name,
                'profile_pk': liker.profile.pk,
                'avatar_url': liker.profile.get_avatar(),
                'display_name': liker.profile.get_name_to_display()
            }
            users_json['data'][index] = data
        return JsonResponse(users_json)
    else:
        return JsonResponse({'message': 'Wrong method for getting list or request not AJAX'}, status=400)