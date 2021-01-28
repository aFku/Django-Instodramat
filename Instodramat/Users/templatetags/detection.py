from django import template

register = template.Library()


@register.filter(name='detect_type')
def detect_type(input_html, type_html=''):
    """
    Check if given input has given type or check if tag has any type
    """
    if len(type_html) == 0:
        return 'type' in str(input_html).lower()
    else:
        return f'type="{type_html}"' in str(input_html).lower()


@register.filter(name='check_if_follow')
def check_if_follow(following_profile, followed_user):
    """
    Check follow field in following_profile and find there followed_user
    Existing of this templatetag is required because cannot compare Auth.model with queryset
    {% if profile.user (Auth.model) in request.user.follow.all (queryset) %}
    """
    from django.contrib.auth.models import User
    followed_user = User.objects.get(pk=followed_user.pk)  # create query with user
    return True if followed_user in following_profile.follow.all() else False
