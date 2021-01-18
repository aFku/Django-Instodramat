from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddPhotoForm, CommentAddForm
from django.contrib import messages
from .models import Photo, Comment


@login_required(login_url='/login')
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

####Create URL with photo_id
@login_required(login_url='/login')
def image_preview(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    form = CommentAddForm()
    comments_set = photo.get_comments()
    if request.method == "POST":
        comment = Comment(**form.cleaned_data, author=request.user, related_photo=photo)
        comment.save()
    return render(request, 'photo_preview.html', {'photo': photo, 'form': form, 'comments': comments_set})
