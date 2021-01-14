from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddPhotoForm
from django.contrib import messages


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

