from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from Images.models import Photo


def main_webpage_view(request):
    if request.user.is_authenticated:
        return main_webpage_auth_view(request)
    else:
        return main_webpage_unauth_view(request)


def main_webpage_auth_view(request):
    user = request.user
    follow_photos = user.profile.get_list_of_latest_follows_photos()
    paginator = Paginator(follow_photos, 10)

    # Shoutbox

    return render(request, 'main_page_auth.html', {'photos': follow_photos})


def main_webpage_unauth_view(request):
    return render(request, 'main_page_unauth.html')


def latest_photos_view(request):
    if request.user.is_authenticated:
        latest_photos = Photo.objects.order_by('publish_date')
        paginator = Paginator(latest_photos, 20)
    else:
        return redirect('/')
