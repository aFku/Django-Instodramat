from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from Images.models import Photo
from Users.models import Profile
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def main_webpage_view(request):
    if request.user.is_authenticated:
        return main_webpage_auth_view(request)
    else:
        return main_webpage_unauth_view(request)


def main_webpage_auth_view(request):
    user = request.user
    follow_photos = user.profile.get_list_of_latest_follows_photos()
    paginator = Paginator(follow_photos, 5)
    p_number = request.GET.get("page")
    page = paginator.get_page(p_number) if p_number else paginator.get_page(1)

    return render(request, 'main_page_auth.html', {'page': page})


def main_webpage_unauth_view(request):
    return render(request, 'main_page_unauth.html')

@login_required
def latest_photos_all_view(request):
    latest_photos = Photo.objects.order_by('publish_date')[:30]
    return render(request, 'latest_photos.html', {'latest_photos': latest_photos})





