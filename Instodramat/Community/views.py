from django.shortcuts import render
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
    latest_photos = Photo.objects.order_by('-publish_date')[:30]
    return render(request, 'latest_photos.html', {'latest_photos': latest_photos})

@csrf_exempt
@login_required
def ajax_search_endpoint(request):
    if request.is_ajax() and request.method == "GET":
        search_input = request.GET.get('searchinput')
        search_result = Profile.objects.filter(Q(first_name__contains=search_input) |
                                               Q(last_name__contains=search_input) |
                                               Q(user__username__contains=search_input))[:5]
        # I tried Django serializer, but this is the best way to include username from profile.user.username to JSON
        search_result = [{'user_pk': result.pk,
                          'display_name': result.get_name_to_display(),
                          'username': result.user.username,
                          'avatar_url': result.get_avatar()
                          } for result in search_result]
        return JsonResponse(search_result, status=200, safe=False)
    else:
        return JsonResponse({
            'message': 'Bad request'
        }, status=405)




